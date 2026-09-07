# Architecture

Browser URL → Flask orchestrator → HTML/DOM extractor → text classifier + visual/behavioral adapters → evidence correlator → risk engine → case/evidence store → React forensic console.

The current package includes the orchestration contract and deterministic demo behavior. Heavy browser/CV/LLM components are intentionally adapter points so the project remains runnable without large model downloads.
