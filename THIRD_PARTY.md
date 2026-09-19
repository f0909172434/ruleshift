# Third-party components

RuleShift code is Apache-2.0. Dependencies retain their own licenses; exact Python and JavaScript dependency versions are recorded in `uv.lock` and `web/package-lock.json`.

- [MLX](https://github.com/ml-explore/mlx) and [MLX LM](https://github.com/ml-explore/mlx-lm): MIT. Local inference runtime; not vendored.
- [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507): Apache-2.0 model. This project downloads the community MLX 4-bit conversion [mlx-community/Qwen3-4B-Instruct-2507-4bit](https://huggingface.co/mlx-community/Qwen3-4B-Instruct-2507-4bit), revision `50d427756c6b1b2fe0c0a10f67fbda1fc8e82c1b`. Model weights and tokenizer assets are not included in this repository or evidence release.
- DM Sans and DM Mono: SIL Open Font License 1.1. Font binaries are supplied through Fontsource and bundled into the built web app. Original copyright notices and licenses are retained in `third_party/*-OFL.txt`.
- React (MIT), Vite (MIT), Lucide (ISC), Gymnasium (MIT), FastAPI (MIT), Pydantic (MIT), NumPy (BSD-3-Clause), and other installed libraries retain their respective upstream terms.

Recruitment descriptions and research papers belong to their original authors/publishers. Documentation links to them and lists factual job titles; no affiliation or endorsement is implied. The recruitment reference used during development is not part of the software/data license grant.
