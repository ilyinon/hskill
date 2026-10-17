"""Check the named offline teaching arithmetic/state contracts, never targets.

Inputs are inert JSON. These checks do not execute skill recipe catalogs,
product runtimes, model providers, kernels, browsers, or financial operations.
"""
import hashlib
import hmac
import json
import math
from pathlib import Path, PurePosixPath
import unittest

SKILLS = Path(__file__).resolve().parents[1] / 'skills'


def data(topic):
    return json.loads((SKILLS / topic / 'references/examples/input.json').read_text())


def lsb_payload(samples, count):
    if len(samples) != count * 8 or any(type(v) is not int or not 0 <= v <= 255 for v in samples):
        raise ValueError('invalid teaching samples')
    output = []
    for offset in range(0, len(samples), 8):
        word = 0
        for sample in samples[offset:offset + 8]:
            word = (word << 1) | (sample & 1)
        output.append(word)
    return bytes(output)


class ExtendedSolving(unittest.TestCase):
    def test_partial_write_preserves_upper_bits(self):
        d = data('arbitrary-write-to-rce')
        mask = (1 << d['write_bits']) - 1
        result = (d['initial'] & ~mask) | (d['requested'] & mask)
        self.assertEqual(result, 0x12340099)
        self.assertNotEqual(result, d['requested'])
        self.assertEqual(result & ~mask, d['initial'] & ~mask)
        self.assertEqual(result, d['control_target'])

    def test_charset_encoding_is_not_low_byte_narrowing(self):
        d = data('ghost-bits-cast-attack')
        point = int(d['code_point'], 16)
        self.assertEqual(point & 255, 13)
        encoded = chr(point).encode('utf-8')
        self.assertEqual(encoded, bytes.fromhex('e7988d'))
        self.assertNotIn(13, encoded)
        self.assertFalse(d['reachable_narrowing_sink'])
        self.assertEqual(encoded.decode('utf-8'), chr(point))

    def test_unsigned_predicate_matches_every_byte(self):
        d = data('code-obfuscation-deobfuscation')
        modulus = 1 << d['bits']
        actual = [x for x in range(modulus) if (x + d['increment']) % modulus < x]
        self.assertEqual(actual, [255])
        self.assertNotIn(d['boundary_inputs'][0], actual)
        self.assertIn(d['boundary_inputs'][1], actual)

    def test_original_finite_word_equation(self):
        d = data('symbolic-execution-tools')
        modulus = 1 << d['bits']
        solutions = [x for x in range(modulus) if (x + d['add']) % modulus == d['target']]
        self.assertEqual(solutions, [242])
        naive = d['target'] - d['add']
        self.assertLess(naive, 0)
        self.assertEqual((solutions[0] + d['add']) & (modulus - 1), d['target'])
        self.assertNotEqual((solutions[0] - 1 + d['add']) % modulus, d['target'])

    def test_vm_operand_byte_order_against_trace(self):
        d = data('vm-and-bytecode-reverse')
        operands = [bytes.fromhex(d[k]) for k in ['operand_hex', 'control_operand_hex']]
        outputs = [int.from_bytes(v, d['byte_order']) + d['add'] for v in operands]
        self.assertEqual(outputs, d['native_outputs'])
        self.assertNotEqual(int.from_bytes(operands[0], 'big') + d['add'], outputs[0])
        self.assertEqual([len(v) for v in operands], [2, 2])

    def test_rotation_and_independent_checksum(self):
        d = data('classical-cipher-analysis')
        def rotate(text, shift):
            return ''.join(chr((ord(c) - 65 + shift) % 26 + 65) for c in text)
        candidates = [(s, rotate(d['ciphertext'], -s)) for s in range(26)]
        valid = [(s, p) for s, p in candidates if len(p) == d['plaintext_length'] and sum(p.encode()) == d['independent_plaintext_byte_sum']]
        self.assertEqual(valid, [(3, 'HELLO')])
        self.assertEqual(rotate(valid[0][1], valid[0][0]), d['ciphertext'])

    def test_hmac_rfc_vector_and_changed_message(self):
        d = data('hash-attack-techniques')
        tag = hmac.new(d['synthetic_key'].encode(), d['message'].encode(), hashlib.sha256).hexdigest()
        self.assertEqual(tag, d['sha256_tag'])
        changed = hmac.new(d['synthetic_key'].encode(), d['modified_message'].encode(), hashlib.sha256).hexdigest()
        self.assertFalse(hmac.compare_digest(changed, tag))
        prefix_hash = hashlib.sha256((d['synthetic_key'] + d['message']).encode()).hexdigest()
        self.assertNotEqual(prefix_hash, tag)

    def test_candidates_against_original_algebra(self):
        d = data('lattice-crypto-attacks')
        def valid(x):
            return (0 <= x < d['upper_bound_exclusive'] and pow(x, d['power'], d['modulus']) == d['residue'] and x % d['record_modulus'] == d['record_residue'])
        self.assertEqual([x for x in d['candidates'] if valid(x)], [4])
        self.assertEqual([x for x in range(d['upper_bound_exclusive']) if valid(x)], [4])
        self.assertEqual(pow(7, d['power'], d['modulus']), d['residue'])
        self.assertFalse(valid(7))

    def test_raw_rsa_shared_factor_and_original_equation(self):
        d = data('rsa-attack-techniques')
        p = math.gcd(d['n'], d['second_modulus'])
        q = d['n'] // p
        self.assertEqual((p, q), (5, 11))
        phi = (p - 1) * (q - 1)
        secret_exponent = pow(d['e'], -1, phi)
        m = pow(d['ciphertext'], secret_exponent, d['n'])
        self.assertEqual(m, 12)
        self.assertEqual(pow(m, d['e'], d['n']), d['ciphertext'])
        self.assertEqual(m % d['record_modulus'], d['record_residue'])
        self.assertEqual([x for x in range(d['n']) if pow(x, d['e'], d['n']) == d['ciphertext']], [m])
        self.assertFalse(any(x ** d['e'] == d['ciphertext'] for x in range(d['n'])))

    def test_lsb_recovery_and_corruption_control(self):
        d = data('steganography-techniques')
        payload = lsb_payload(d['samples'], d['payload_bytes'])
        self.assertEqual(payload, b'OK')
        self.assertEqual(sum(payload), d['independent_byte_sum'])
        corrupt = d['samples'][:]; corrupt[0] ^= 1
        self.assertNotEqual(sum(lsb_payload(corrupt, d['payload_bytes'])), d['independent_byte_sum'])
        with self.assertRaises(ValueError):
            lsb_payload(d['samples'][:-1], d['payload_bytes'])

    def test_membership_accuracy_against_majority_baseline(self):
        d = data('ai-ml-security')
        total = d['members'] + d['nonmembers']
        self.assertEqual(d['true_positive'] + d['false_negative'], d['members'])
        self.assertEqual(d['true_negative'] + d['false_positive'], d['nonmembers'])
        accuracy = (d['true_positive'] + d['true_negative']) / total
        self.assertEqual(accuracy, d['nonmembers'] / total)
        sensitivity = d['true_positive'] / d['members']
        specificity = d['true_negative'] / d['nonmembers']
        self.assertEqual(sensitivity, 0)
        self.assertEqual((sensitivity + specificity) / 2, 0.5)

    def test_settled_net_balance_without_double_count(self):
        d = data('defi-attack-patterns')
        final = d['owned_before_fee'] - d['outstanding_fee']
        self.assertEqual(final, 99)
        self.assertEqual(final - d['initial_owned'], -1)
        self.assertGreater(d['owned_before_fee'], d['initial_owned'])

    def test_canonical_path_components_not_text_prefix(self):
        d = data('path-traversal-lfi')
        root = PurePosixPath(d['root'])
        candidate = PurePosixPath(d['candidate'])
        self.assertTrue(str(candidate).startswith(str(root)))
        self.assertFalse(candidate.is_relative_to(root))
        self.assertTrue(PurePosixPath(d['inside_control']).is_relative_to(root))
        self.assertFalse(PurePosixPath('/srv/exports-other').is_relative_to(root))

    def test_process_instance_lifetime_and_ambiguity(self):
        d = data('memory-forensics-volatility')
        def matches(pid, when=None, object_id=None):
            return [p['object'] for p in d['processes'] if p['pid'] == pid and (when is None or p['start'] <= when < p['end']) and (object_id is None or p['object'] == object_id)]
        event = d['connection']
        self.assertEqual(matches(event['pid'], event['opened'], event['owner_object']), ['P1'])
        self.assertEqual(matches(event['pid']), ['P1', 'P2'])
        self.assertEqual(matches(event['pid'], 220), ['P2'])
        self.assertEqual(matches(event['pid'], 170), [])
        self.assertEqual(matches(event['pid'], event['opened'], 'P2'), [])

    def test_interleaving_and_atomic_consumption(self):
        d = data('race-condition')
        def apply(events, atomic):
            used = False; checks = {}; ledger = []
            for client, action in events:
                if action == 'check':
                    checks[client] = not used
                elif checks.get(client) and (not atomic or not used):
                    ledger.append((client, d['credit'])); used = True
            return used, sum(amount for _, amount in ledger)
        self.assertEqual(apply(d['events'], False), (True, 20))
        self.assertEqual(apply(d['sequential_control'], False), (True, 10))
        self.assertEqual(apply(d['events'], True), (True, 10))
        self.assertEqual(apply(d['sequential_control'], True), (True, 10))
