# ai-ml-security technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 9. DECISION TREE

```
Assessing an AI/ML system?
├── Is there a model loading / deployment pipeline?
│   ├── Yes → Check supply chain (Section 1)
│   │   ├── Model format? → .pt/.pkl = pickle risk (Section 1.1)
│   │   │   └── SafeTensors / ONNX? → Lower risk
│   │   ├── Source? → Hugging Face / external → verify provenance (Section 1.2)
│   │   │   └── trust_remote_code=True? → HIGH RISK
│   │   └── Dependencies? → Check for confusion attacks (Section 1.3)
│   └── No (API only) → Skip to usage-level attacks
├── Is it a classification / detection model?
│   ├── Yes → Test adversarial robustness (Section 2)
│   │   ├── White-box access? → FGSM/PGD/C&W
│   │   ├── Black-box API? → Transfer attacks, query-based
│   │   └── Physical deployment? → Adversarial patches (Section 2.5)
│   └── No → Continue
├── Is it trained on user-contributed data?
│   ├── Yes → Data poisoning risk (Section 3)
│   │   ├── Federated learning? → Gradient manipulation (Section 3.3)
│   │   └── Centralized? → Training data integrity verification
│   └── No → Continue
├── Is it an API / MLaaS?
│   ├── Yes → Model extraction risk (Section 4)
│   │   ├── Returns confidence scores? → Higher extraction risk
│   │   └── Rate limiting? → Slows but doesn't prevent extraction
│   └── No → Continue
├── Is it trained on sensitive data?
│   ├── Yes → Privacy attacks (Section 5)
│   │   ├── Membership inference (Section 5.1)
│   │   ├── Model inversion (Section 5.2)
│   │   └── Federated? → Gradient leakage (Section 5.3)
│   └── No → Continue
├── Is it an LLM / chatbot?
│   ├── Yes → Load [llm-prompt-injection](../llm-prompt-injection/SKILL.md)
│   │   └── Also check training data extraction (Section 6.1)
│   └── No → Continue
├── Is it an autonomous agent?
│   ├── Yes → Agent security (Section 7)
│   │   ├── What tools does it have access to?
│   │   ├── Does it interact with other agents?
│   │   └── Is user confirmation required for side effects?
│   └── No → Continue
└── Run automated scanning (Section 8)
    ├── Fickling / ModelScan for model file safety
    ├── ART for adversarial robustness
    └── Garak / PyRIT for LLM-specific vulnerabilities
```
