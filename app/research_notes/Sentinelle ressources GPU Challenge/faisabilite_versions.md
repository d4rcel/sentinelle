# Technical feasibility and version compatibility of the GPU ML stack (RAPIDS, XGBoost, PyTorch, PyG, FastAPI, Streamlit)

Research date: 2026-11-19. All version numbers below were read on that date from PyPI JSON, official install pages, wheel indexes or Docker Hub API. "VERIFIED" = seen in the cited page/API. Anything not seen is in Inferences or Gaps.
Note: `docs.rapids.ai/*` now redirects to `docs.nvidia.com/datascience/*` ("NVIDIA CUDA-X libraries for data science").

## 1. Current stable versions (Nov 2026) and their Python / CUDA / driver / GPU / OS requirements

### Takeaway
RAPIDS stable is 26.10 (26.12 ships 9-10 Dec 2026, i.e. after the hackathon), XGBoost 3.4.1, PyTorch 2.15.0, torch-geometric 2.8.1. The whole stack is Linux-first (glibc >= 2.28, Windows only through WSL2 for RAPIDS), needs an NVIDIA GPU with compute capability >= 7.0 (Volta; CUDA 13 builds need Turing or newer) and driver >= 525/535 for CUDA 12 or >= 580 for CUDA 13.

### Cited Findings

RAPIDS (VERIFIED)
- Install selector: Stable = 26.10, Nightly = 26.12a; methods Conda / pip / Docker; CUDA "12.2 - 12.9" or "13.0 - 13.3"; Python 3.11, 3.12, 3.13, 3.14 for stable (nightly 26.12: 3.12-3.14 only, 3.11 dropped) — [RAPIDS install](https://docs.rapids.ai/install/)
- Release 26.12 schedule: code freeze 17/24 Nov 2026, release Wed 9 Dec - Thu 10 Dec 2026, so 26.10 is still the stable release on 25-26 Nov 2026 — [RAPIDS maintainers / release schedule](https://docs.rapids.ai/maintainers/)
- GPU requirement: "NVIDIA Volta or higher with compute capability 7.0+"; Pascal support removed in 24.02 — [RAPIDS install](https://docs.rapids.ai/install/)
- Per-release table for 26.10: Linux glibc 2.28+ x86_64 and aarch64 (tested Ubuntu 22.04/24.04/26.04, Rocky 8); Windows via WSL only; CUDA 12 toolkit 12.2-12.9, driver 535+, compute capability Volta(70), Turing(75), Ampere(80,86), Ada(89), Hopper(90), Blackwell(100,120); CUDA 13 toolkit 13.0-13.3, driver 580+, Turing(75) or newer only (no Volta) — [RAPIDS platform support](https://docs.rapids.ai/platform-support/)
- Conflict between two official pages on the CUDA 12 minimum driver: install page says "CUDA 12 with Driver 525.60.13 or newer / CUDA 13 with Driver 580.65.06 or newer" — [RAPIDS install](https://docs.rapids.ai/install/); platform-support table says "535+" for CUDA 12 — [RAPIDS platform support](https://docs.rapids.ai/platform-support/). NVIDIA's generic table: CUDA 12.x >= 525, CUDA 13.x >= 580 — [CUDA compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)
- WSL2: Windows 11 + WSL2 Ubuntu, single GPU only, no GPU Direct Storage, 16 GB+ GPU RAM recommended — [RAPIDS install](https://docs.rapids.ai/install/)
- PyPI: `cudf-cu12` 26.10.2 and `cudf-cu13` 26.10.2 (uploaded 2026-10-22), requires_python >=3.11, wheels are `cp311-abi3` manylinux_2_28 x86_64 + aarch64 only (no Windows/macOS wheels). Deps: `numpy<3.0,>=2.0`, `pandas<3.1.0,>=3.0.0`, `numba<0.65.0,>=0.60.0`, `numba-cuda[cu12]<0.31.0,>=0.22.2`, `cupy-cuda12x[ctk]!=14.1.0,>=14.0.1`, `pyarrow>=19.0.0`, `cuda-bindings<13.0,>=12.9.2` — [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json), [PyPI cudf-cu13](https://pypi.org/pypi/cudf-cu13/json)
- `cuml-cu12` / `cuml-cu13` 26.10.0 (2026-10-08), requires_python >=3.11, abi3 wheel; classifiers list only Python 3.11 and 3.12; deps `scikit-learn>=1.6`, `scipy>=1.14.0`, `treelite<5.0.0,>=4.7.2`, `cuda-toolkit[cublas,cufft,curand,cusolver,cusparse]==12.*` (resp. `==13.*`), `nvidia-nvjitlink-cu12<13,>=12.9` (resp. `nvidia-nvjitlink<14,>=13.3`) — [PyPI cuml-cu12](https://pypi.org/pypi/cuml-cu12/json), [PyPI cuml-cu13](https://pypi.org/pypi/cuml-cu13/json)
- `cugraph-cu12` / `cugraph-cu13` 26.10.0, requires_python >=3.11 — [PyPI cugraph-cu12](https://pypi.org/pypi/cugraph-cu12/json), [PyPI cugraph-cu13](https://pypi.org/pypi/cugraph-cu13/json)
- `cugraph-pyg-cu12` / `-cu13` 26.10.0, pure-python wheel (`py3-none-any`), requires_python >=3.11, deps `pylibcugraph-cuXX==26.10.*`, `pylibwholegraph-cuXX==26.10.*`, cupy, numpy>=2, pandas; it declares NO dependency on torch or torch-geometric (user must install them) — [PyPI cugraph-pyg-cu12](https://pypi.org/pypi/cugraph-pyg-cu12/json), [PyPI cugraph-pyg-cu13](https://pypi.org/pypi/cugraph-pyg-cu13/json)

XGBoost (VERIFIED)
- `xgboost` 3.4.1 (uploaded 2026-08-15), requires_python >=3.12, classifiers 3.12/3.13/3.14, wheels `py3-none` for manylinux_2_28 x86_64/aarch64, macOS, win_amd64, win_arm64; depends on `nvidia-nccl-cu13` on Linux; largest wheel 57.6 MB — [PyPI xgboost](https://pypi.org/pypi/xgboost/json)
- "The default xgboost wheel for Linux x86_64 and aarch64 is built with CUDA Toolkit 13.x"; for drivers that support CUDA 12 but not 13: `pip install xgboost-cu12`; CPU-only small package: `pip install xgboost-cpu`. GPU supported in wheels on Linux x86_64, Linux aarch64 and Windows x86_64 (no multi-GPU on Windows); no GPU on macOS — [XGBoost install](https://xgboost.readthedocs.io/en/stable/install.html)
- `xgboost-cu12` 3.4.1, requires_python >=3.12, 83.5 MB manylinux_2_28_x86_64 wheel — [PyPI xgboost-cu12](https://pypi.org/pypi/xgboost-cu12/json); `xgboost-cpu` 3.4.1, 5.8 MB — [PyPI xgboost-cpu](https://pypi.org/pypi/xgboost-cpu/json)
- Version discrepancy: PyPI latest is 3.4.1 — [PyPI xgboost](https://pypi.org/pypi/xgboost/json); the "stable" docs page title reads "xgboost 3.4.2 documentation" — [XGBoost GPU SHAP example](https://xgboost.readthedocs.io/en/stable/python/examples/gpu_tree_shap.html)

PyTorch (VERIFIED)
- `torch` 2.15.0 (uploaded 2026-10-28), requires_python >=3.11, wheels cp311-cp315, Linux x86_64/aarch64 manylinux_2_28, macOS arm64, win_amd64. The default PyPI Linux wheel is a CUDA 13.2 build: `cuda-toolkit[...]==13.2.2`, `nvidia-cudnn-cu13==9.26.0.51`, `nvidia-nccl-cu13==2.30.7`; wheel up to 539 MB — [PyPI torch](https://pypi.org/pypi/torch/json)
- Stable selector commands embedded in the get-started page: `pip3 install torch torchvision` (default), `--index-url https://download.pytorch.org/whl/cpu`, `.../whl/cu132`, `.../whl/cu134`, `.../whl/rocm10.0`. No CUDA 12 option is offered for the current stable — [PyTorch get started](https://pytorch.org/get-started/locally/)
- Wheel indexes confirm it: `torch-2.15.0` exists under `cu132`, `cu134` and `cpu` — [cu132 index](https://download.pytorch.org/whl/cu132/torch/), [cu134 index](https://download.pytorch.org/whl/cu134/torch/), [cpu index](https://download.pytorch.org/whl/cpu/torch/); the `cu126` and `cu130` indexes stop at torch 2.14.1 — [cu126 index](https://download.pytorch.org/whl/cu126/torch/), [cu130 index](https://download.pytorch.org/whl/cu130/torch/)
- Last release with a CUDA 12 build: 2.14.1 — `pip install torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cu126` (also cu130, cu132, cpu) — [PyTorch previous versions](https://pytorch.org/get-started/previous-versions/); `torch-2.14.1+cu126` wheels exist for cp310-cp315 — [cu126 index](https://download.pytorch.org/whl/cu126/torch/)
- Linux requirement glibc >= 2.28; Python "3.10 - 3.14" recommended in page text — [PyTorch get started](https://pytorch.org/get-started/locally/)

PyTorch Geometric (VERIFIED)
- `torch-geometric` 2.8.1 (uploaded 2026-10-12), pure-python wheel, requires_python >=3.10, classifiers 3.10-3.14; core deps: aiohttp, fsspec, jinja2, numpy, psutil, pyparsing, requests, tqdm, xxhash (torch is not declared as a dependency) — [PyPI torch-geometric](https://pypi.org/pypi/torch-geometric/json)
- "From PyG 2.3 onwards, you can install and use PyG without any external library required except for PyTorch": `pip install torch_geometric`. Optional: `pip install pyg_lib torch_scatter torch_sparse -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html`. "`torch-cluster` and `torch-spline-conv` are no longer required as separate packages. Their functionality has been migrated to `pyg-lib>=0.6.0`." The page's selector/list tops out at PyTorch 2.12.* (cpu|cu126|cu130|cu132) — [PyG installation](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
- The wheel index is ahead of the docs page: it has directories up to `torch-2.14.0+{cpu,cu126,cu130,cu132}`; there is no `torch-2.15.*` directory — [data.pyg.org/whl](https://data.pyg.org/whl/)
- For torch 2.14.0 the only Linux x86_64 extension wheel present is `pyg_lib-0.9.0+pt214cu132-cp310-abi3` (and `+pt214cu126`); no `torch_scatter` / `torch_sparse` wheels in those two indexes — [torch-2.14.0+cu132](https://data.pyg.org/whl/torch-2.14.0+cu132.html), [torch-2.14.0+cu126](https://data.pyg.org/whl/torch-2.14.0%2Bcu126.html). For torch 2.12.0+cu126 `torch_scatter-2.1.2` and `torch_sparse-0.6.18` exist — [torch-2.12.0+cu126](https://data.pyg.org/whl/torch-2.12.0+cu126.html)
- `pyg-lib` is not on PyPI (404) — [PyPI pyg-lib](https://pypi.org/pypi/pyg-lib/json)

Web/demo and misc (VERIFIED, all from PyPI JSON)
- `fastapi` 0.165.0 (2026-11-18), requires_python >=3.11, deps `starlette>=1.6.0`, `pydantic>=2.9.0` — [PyPI fastapi](https://pypi.org/pypi/fastapi/json)
- `streamlit` 1.67.0 (2026-11-05), requires_python >=3.11, deps `numpy<3,>=1.25.0`, `pandas<4,>=1.5.3`, `pyarrow!=25.0.0,<27,>=12.0.0`, `starlette<2,>=0.46.0` — [PyPI streamlit](https://pypi.org/pypi/streamlit/json)
- `uvicorn` 0.54.0, requires_python >=3.10 — [PyPI uvicorn](https://pypi.org/pypi/uvicorn/json)
- `shap` 0.54.1 (2026-10-16), requires_python >=3.12, `cp312-abi3` wheels (+ cp314t/cp315), deps `numpy>=2`, scipy, scikit-learn, pandas — [PyPI shap](https://pypi.org/pypi/shap/json)
- `scikit-learn` 1.9.1 (2026-09-10), requires_python >=3.11, wheels cp311-cp315 — [PyPI scikit-learn](https://pypi.org/pypi/scikit-learn/json)
- `kagglehub` 1.0.3 (2026-10-21), requires_python >=3.11 — [PyPI kagglehub](https://pypi.org/pypi/kagglehub/json); `kaggle` 2.2.5 (2026-10-22), requires_python >=3.11 — [PyPI kaggle](https://pypi.org/pypi/kaggle/json)
- `numpy` 2.5.5 (requires_python >=3.12) — [PyPI numpy](https://pypi.org/pypi/numpy/json); `pandas` 3.1.1 (>=3.11; 3.0.x line goes up to 3.0.6) — [PyPI pandas](https://pypi.org/pypi/pandas/json); `polars` 2.1.0 (>=3.11) — [PyPI polars](https://pypi.org/pypi/polars/json); `pyarrow` 26.0.1 — [PyPI pyarrow](https://pypi.org/pypi/pyarrow/json); `cupy-cuda12x` / `cupy-cuda13x` 14.2.0 (`numpy<2.6,>=2.0`, wheels cp310-cp314) — [PyPI cupy-cuda12x](https://pypi.org/pypi/cupy-cuda12x/json), [PyPI cupy-cuda13x](https://pypi.org/pypi/cupy-cuda13x/json); `numba` 0.68.1 latest, 0.64.0 requires `numpy<2.5,>=1.22` — [PyPI numba](https://pypi.org/pypi/numba/json), [PyPI numba 0.64.0](https://pypi.org/pypi/numba/0.64.0/json)

### Inferences
- A Tesla T4 (Turing, CC 7.5) and anything newer satisfies both the CUDA 12 and CUDA 13 RAPIDS builds; a V100 (Volta) would only work with the CUDA 12 builds; a P100 (Pascal, as on Kaggle) is below the RAPIDS minimum.
- The whole ecosystem moved its default to CUDA 13 during 2026 (torch 2.15 = cu132/cu134 only, xgboost default wheel = CUDA 13). CUDA 13 requires driver >= 580, so the hackathon machines' driver version (shown by `nvidia-smi`) is the single most important unknown.
- RAPIDS pip wheels exist only for Linux: nothing RAPIDS-related can be pip-installed on native Windows or macOS.

### Gaps
- cugraph-pyg's supported torch / torch-geometric version range: the official doc URLs tried returned "Page Not Found" or empty content (https://docs.rapids.ai/api/cugraph-pyg/stable/), and the wheel metadata declares no torch bound. Not verified.
- PyTorch's minimum GPU compute capability for the 2.15 cu132/cu134 binaries was not found on the pages read.
- XGBoost minimum driver / compute capability is not stated on its install page beyond "driver supports CUDA 12 / CUDA 13".
- Whether xgboost 3.4.2 is actually released (docs title vs PyPI disagree).

## 2. A concrete, mutually compatible version set and official install commands; known conflicts

### Takeaway
Two coherent sets exist: a CUDA 13 set (driver >= 580: RAPIDS 26.10 `-cu13` + torch 2.15.0 default + xgboost 3.4.1 default) and a CUDA 12 fallback (driver 525/535-579: RAPIDS 26.10 `-cu12` + torch 2.14.1+cu126 + `xgboost-cu12` 3.4.1). Python 3.12 or 3.13 is the safe interpreter for both; key pins forced by cuDF are pandas 3.0.x (not 3.1), numba < 0.65 and therefore numpy < 2.5.

### Cited Findings

Official commands (VERIFIED, read from the selector's source on the install page)
- Conda (default selector output): `conda create -n rapids-26.10 -c rapidsai -c conda-forge rapids=26.10 python=3.14 'cuda-version>=13.0,<=13.3'` (CUDA 12 variant: `'cuda-version>=12.2,<=12.9'`); `conda activate rapids-26.10`. "Standard" = cuDF, cuML, cuGraph, nx-cugraph, cuCIM, RAFT, cuVS. The selector's optional "PyTorch" add-on appends `'pytorch=*=*cuda*'` to the same conda command, with the note "Third-party packages are not tested." Miniforge is the recommended conda; the `defaults` channel is unsupported — [RAPIDS install](https://docs.rapids.ai/install/)
- pip (stable): `pip install --extra-index-url=https://pypi.nvidia.com "cudf-cu13==26.10.*" "cuml-cu13==26.10.*" "cugraph-cu13==26.10.*" ...` (suffix `-cu12` for CUDA 12). The selector drops the extra index when only cudf, cuml, dask-cudf, raft, nvforest are selected because those are on PyPI; cugraph needs `pypi.nvidia.com`. "pip installations require using a wheel matching the system's installed CUDA toolkit" — [RAPIDS install](https://docs.rapids.ai/install/)
- Docker: `docker run --gpus all --pull always --rm -it --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 nvcr.io/nvidia/rapidsai/base:26.10-cuda13-py3.14` (notebooks variant adds `-p 8888:8888 -p 8787:8787 -p 8786:8786` and uses `rapidsai/notebooks`); Docker Hub equivalent is `rapidsai/base:<tag>`. From 26.12 the `-py<python>` suffix is dropped from tags — [RAPIDS install](https://docs.rapids.ai/install/)
- PyTorch stable: `pip3 install torch torchvision` (CUDA 13.2 build from PyPI), or `--index-url https://download.pytorch.org/whl/cu132` / `cu134` / `cpu` — [PyTorch get started](https://pytorch.org/get-started/locally/)
- PyTorch CUDA 12: `pip install torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cu126` — [PyTorch previous versions](https://pytorch.org/get-started/previous-versions/)
- PyG: `pip install torch_geometric`; optional `pip install pyg_lib torch_scatter torch_sparse -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html` — [PyG installation](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
- XGBoost: `pip install xgboost` (CUDA 13), `pip install xgboost-cu12`, `pip install xgboost-cpu`, or `conda install -c conda-forge py-xgboost=*=cuda*` — [XGBoost install](https://xgboost.readthedocs.io/en/stable/install.html)

Constraints that shape the pin set (VERIFIED metadata)
- cuDF 26.10 requires `pandas<3.1.0,>=3.0.0` while latest pandas is 3.1.1 → pandas must be 3.0.x (latest 3.0.6) — [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json), [PyPI pandas](https://pypi.org/pypi/pandas/json)
- cuDF 26.10 requires `numba<0.65.0,>=0.60.0`; numba 0.64.0 requires `numpy<2.5` → numpy must be 2.0-2.4.x, not the latest 2.5.5 — [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json), [PyPI numba 0.64.0](https://pypi.org/pypi/numba/0.64.0/json)
- cuDF/cuML require `numpy>=2.0` (numpy 1.x is no longer possible); shap 0.54.1 requires `numpy>=2` too — [PyPI cuml-cu12](https://pypi.org/pypi/cuml-cu12/json), [PyPI shap](https://pypi.org/pypi/shap/json)
- Python floor: xgboost 3.4.1 and shap 0.54.1 need >=3.12; RAPIDS 26.10, torch 2.15, fastapi, streamlit, scikit-learn need >=3.11 → intersection is Python 3.12-3.14 — [PyPI xgboost](https://pypi.org/pypi/xgboost/json), [PyPI shap](https://pypi.org/pypi/shap/json), [RAPIDS platform support](https://docs.rapids.ai/platform-support/)
- CUDA 13 coexistence in one pip env: torch 2.15.0 pins `cuda-toolkit[...]==13.2.2`; RAPIDS cu13 wheels ask for `cuda-toolkit[...]==13.*` and `nvidia-nvjitlink<14,>=13.3`; `cuda-toolkit` 13.2.2 itself only requires `nvidia-nvjitlink<14,>=13.2.86` → the constraints overlap (toolkit 13.2.2 + nvjitlink >= 13.3) — [PyPI torch](https://pypi.org/pypi/torch/json), [PyPI libcudf-cu13](https://pypi.org/pypi/libcudf-cu13/json), [PyPI cuda-toolkit 13.2.2](https://pypi.org/pypi/cuda-toolkit/13.2.2/json)
- RAPIDS pip wheels "are not compatible with Tensorflow pip packages" and need NVRTC (in Docker: the `devel` flavour of `nvidia/cuda`, not `base`/`runtime`) — [RAPIDS install](https://docs.rapids.ai/install/)
- pyg_lib prebuilt wheels stop at torch 2.14.0 → with torch 2.15.0 only pure `torch_geometric` is available without compiling — [data.pyg.org/whl](https://data.pyg.org/whl/)
- torch-geometric's `full` extra pins `numba<0.60.0`, which contradicts cuDF's `numba>=0.60.0` → never install `torch_geometric[full]` in the RAPIDS env — [PyPI torch-geometric](https://pypi.org/pypi/torch-geometric/json), [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json)

### Inferences
Proposed sets (assembled by me from the verified metadata above; NOT test-installed, since nothing may be installed on the laptop and it has no GPU):

- Set A, "CUDA 13" (driver >= 580, GPU Turing/T4 or newer), Python 3.12:
  `pip install --extra-index-url=https://pypi.nvidia.com "cudf-cu13==26.10.*" "cuml-cu13==26.10.*" "cugraph-cu13==26.10.*"`
  `pip install torch==2.15.0` (PyPI default = CUDA 13.2) ; `pip install torch_geometric==2.8.1`
  `pip install xgboost==3.4.1 shap==0.54.1 scikit-learn==1.9.1 fastapi==0.165.0 "uvicorn" streamlit==1.67.0 kagglehub==1.0.3`
  Expected resolver outcome: pandas 3.0.x, numpy 2.4.x, numba 0.64.x, cupy-cuda13x 14.2.0. If pyg_lib is wanted, use `torch==2.14.1` from `https://download.pytorch.org/whl/cu132` plus `pip install pyg_lib -f https://data.pyg.org/whl/torch-2.14.0+cu132.html`.
- Set B, "CUDA 12" (driver 525/535-579, or a Volta GPU), Python 3.12:
  `pip install --extra-index-url=https://pypi.nvidia.com "cudf-cu12==26.10.*" "cuml-cu12==26.10.*" "cugraph-cu12==26.10.*"`
  `pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cu126` ; `pip install torch_geometric==2.8.1` ; optional `pip install pyg_lib -f https://data.pyg.org/whl/torch-2.14.0+cu126.html`
  `pip install xgboost-cu12==3.4.1` + the same CPU-side packages.
- Risk for Set B: RAPIDS cu12 wants `nvidia-nvjitlink-cu12>=12.9` and `cuda-toolkit==12.*` while a cu126 torch build normally pins CUDA 12.6 component wheels; a pip conflict between the two is plausible. I did not read the dependency metadata of the `torch-2.14.1+cu126` wheel, so this is unconfirmed. Mitigations: (a) the conda route, where the RAPIDS selector officially offers `'pytorch=*=*cuda*'` in the same solve; (b) two virtualenvs (RAPIDS+XGBoost for tabular features, torch+PyG for the GNN) exchanging Parquet/NumPy files.
- Python choice: 3.12 is the most conservative (lowest version accepted by every package, still supported by RAPIDS 26.12 nightly, listed in cuML classifiers). 3.13 is equally valid by metadata.
- Because the default `xgboost` wheel is CUDA 13, installing plain `xgboost` on a driver < 580 machine would give a GPU-unusable build; use `xgboost-cu12` there (uninstall the other first, as the docs show).

### Gaps
- No end-to-end install of either set was executed (constraint: no installs, no GPU). The team should validate Set A/B once on Colab or Kaggle before the event.
- Dependency pins of `torch==2.14.1+cu126` (not on PyPI; index metadata not read).
- Whether the conda-forge `pytorch` CUDA build co-solves with `rapids=26.10` today (selector says such third-party additions "are not tested").
- torch-geometric 2.8.1's officially tested torch range (the PyG install page only lists up to 2.12.*; no statement for 2.15).

## 3. Free GPU options today and their real limits

### Takeaway
Kaggle (documented 30 h/week GPU quota, T4 x2 or P100, cuDF/cuML preinstalled) and Google Colab free (cuDF preinstalled, limits unpublished, max 12 h sessions) are the two realistic zero-cost GPU rehearsal environments; Lightning AI and Modal add small monthly free allowances. Hugging Face Spaces is no longer a free host for a Streamlit/Docker demo.

### Cited Findings
- Colab: free tier gives GPU access but "Colab does not publish these limits"; idle timeouts, max VM lifetime and GPU types "vary over time"; "notebooks can run for at most 12 hours, depending on availability and your usage patterns"; free tier has "a standard system memory profile"; web-UI/content-generation use on free runtimes can be terminated — [Colab FAQ](https://research.google.com/colaboratory/faq.html)
- "cuDF is preinstalled on Google Colab and instantly accelerates Pandas with zero code changes"; full RAPIDS install on Colab is by pip via `!git clone https://github.com/rapidsai/rapidsai-csp-utils.git` then `!python rapidsai-csp-utils/colab/pip-install.py` (installs latest stable cuDF, cuML, cuGraph and xgboost; "a few minutes"; the script may pin RAPIDS versions) — [RAPIDS on Colab](https://docs.rapids.ai/deployment/stable/platforms/colab/)
- Kaggle session specs: 12 h execution time for CPU/GPU sessions, 20 GB auto-saved disk (`/kaggle/working`), CPU sessions 30 GB RAM; "P100 GPU: 1 Nvidia Tesla P100, 29 GB RAM"; "T4 x2 GPU: 2 Nvidia Tesla T4, 29 GB RAM"; 20 min idle timeout in the editor; images updated about every two weeks — [Kaggle Notebooks docs](https://www.kaggle.com/docs/notebooks)
- Kaggle GPU quota: "The quota resets weekly and is 30 hours or sometimes higher depending on demand and resources"; interactive sessions stay active until a 60 minute idle timeout — [Kaggle efficient GPU usage](https://www.kaggle.com/docs/efficient-gpu-usage). (The two Kaggle pages give different idle timeouts: 20 min vs 60 min.)
- "The latest Kaggle notebook environment includes libraries such as cuDF and cuML, so you can start using them without a separate installation"; choose Accelerator "GPU T4 x2 or GPU P100" and "Always use latest environment" — [RAPIDS on Kaggle](https://docs.rapids.ai/deployment/stable/platforms/kaggle/)
- Kaggle's image is built FROM the Colab runtime image (`us-docker.pkg.dev/colab-images/public/runtime:release-colab-external-images_20261027-...`) — [Kaggle docker-python Dockerfile.tmpl](https://raw.githubusercontent.com/Kaggle/docker-python/main/Dockerfile.tmpl)
- Kaggle P100 is Pascal; RAPIDS removed Pascal support in 24.02 — [RAPIDS install](https://docs.rapids.ai/install/)
- SageMaker Studio Lab: account by request, a mobile phone number must be associated on first runtime start; "You are allotted 15 GB of storage and 16 GB of RAM. Availability of compute instances is not guaranteed"; CPU or GPU runtime choice — [AWS Studio Lab overview](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-lab-overview.html). Listed by RAPIDS as a free/limited trial option together with Colab and Paperspace — [RAPIDS install](https://docs.rapids.ai/install/)
- Lightning AI: "Get up to 50 free GPU hours"; "Run 1 Studio free 24/7. No credit card"; "Free Studios run 24/7 but require restart every 4 hours"; "Free hours plus up to 30 credits to start"; T4 16 GB listed at $0.55/hr — [Lightning pricing](https://lightning.ai/pricing)
- Modal: Starter plan "$0 + compute / month" with "$30 / month free credits"; T4 at $0.000164/sec — [Modal pricing](https://modal.com/pricing)
- Paperspace (DigitalOcean) Notebooks "include a free GPU plan"; "When using free-tier machines, the maximum auto-shutdown timeout is 6 hours" — [Paperspace Notebooks features](https://docs.digitalocean.com/products/paperspace/notebooks/details/features/)
- Hugging Face Spaces: "Static Spaces are free for everyone. Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts"; CPU Basic (2 vCPU, 16 GB, 50 GB non-persistent disk) has no hourly cost but creating a compute Space needs a paid plan; SDK options are Gradio, Docker and static HTML (Streamlit is not listed as an SDK); T4 small $0.40/h — [HF Spaces overview](https://huggingface.co/docs/hub/spaces-overview), [HF Spaces GPUs](https://huggingface.co/docs/hub/spaces-gpus)

### Inferences
- On Kaggle, pick "GPU T4 x2" (Turing) for RAPIDS work, not P100.
- Modal's $30/month at $0.000164/s for a T4 is roughly 50 T4-hours per month (30 / (0.000164 x 3600) = about 50.8 h).
- For a public Streamlit demo, Streamlit Community Cloud (GitHub-connected) is the natural free host now that HF compute Spaces need a paid plan; a CPU-only FastAPI + XGBoost scorer fits any of these.

### Gaps
- Colab free GPU model (T4 16 GB) and exact quotas: not published by Google; the FAQ never names the GPU. Unverified.
- Whether `%load_ext cudf.pandas` works out of the box on Colab/Kaggle today and which RAPIDS, XGBoost, torch, torch-geometric versions are preinstalled: not listed on the pages read (`kaggle_requirements.txt` in Kaggle/docker-python does not list cudf, xgboost or torch-geometric; they would come from the Colab base image). Check with `pip list` in a live session.
- Kaggle phone verification requirement for GPU/internet: not found in the docs pages fetched (no "phone" text in https://www.kaggle.com/docs/notebooks as rendered).
- SageMaker Studio Lab GPU type and session/daily hour limits: the Studio Lab FAQ (https://studiolab.sagemaker.aws/faq) returned HTTP 403; not verified.
- Paperspace free-tier GPU types and current availability; NVIDIA DLI / build.nvidia.com credits; Streamlit Community Cloud resource limits: not verified.

## 4. What runs CPU-only on the laptop, and writing code portable between CPU and GPU

### Takeaway
Everything except RAPIDS itself can be developed on the laptop: XGBoost `hist` on CPU, PyTorch CPU + PyG, FastAPI and Streamlit all have CPU wheels. Portability is by design: XGBoost switches with the single `device` parameter and models load on any device, and `cudf.pandas` runs unchanged pandas code with automatic CPU fallback.

### Cited Findings
- XGBoost GPU is enabled by `device="cuda"` with `tree_method="hist"` (`XGBRegressor(tree_method="hist", device="cuda")`; `cuda:<ordinal>` selects a GPU); `QuantileDMatrix` is recommended to reduce memory — [XGBoost GPU support](https://xgboost.readthedocs.io/en/stable/gpu/index.html)
- "The model can be used on any device regardless of the one used to train it. For instance, a model trained using GPU can still work on a CPU-only machine and vice versa" — [XGBoost GPU support](https://xgboost.readthedocs.io/en/stable/gpu/index.html)
- `cudf.pandas` "supports 100% of the Pandas API, using the GPU for supported operations, and automatically falling back to pandas for other operations"; enable with `%load_ext cudf.pandas` in Jupyter, `python -m cudf.pandas script.py`, or `cudf.pandas.install()`; "Nothing changes, not even your import statements" — [cudf.pandas docs](https://docs.rapids.ai/api/cudf/stable/cudf_pandas/)
- `cudf.pandas` passes 93% of 187,000+ pandas unit tests; CI-tested with PyTorch, scikit-learn and XGBoost among third-party libraries; fallback copies data GPU<->CPU, so GPU-only code paths are faster; a profiler shows which calls ran on GPU vs CPU — [cudf.pandas FAQ](https://docs.rapids.ai/api/cudf/stable/cudf_pandas/faq/)
- CPU-only builds exist: `pip install xgboost-cpu` (5.8 MB wheel) and `pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu`; PyG needs only PyTorch (`pip install torch_geometric`) — [XGBoost install](https://xgboost.readthedocs.io/en/stable/install.html), [PyTorch get started](https://pytorch.org/get-started/locally/), [PyG installation](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
- cuDF 26.10 targets pandas 3.0.x (`pandas<3.1.0,>=3.0.0`) — [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json)

### Inferences
- Minimal portability pattern: pick the device once (e.g. `device = "cuda" if torch.cuda.is_available() else "cpu"`), pass it to XGBoost and to `.to(device)` in PyTorch/PyG; write feature engineering in plain pandas and enable `cudf.pandas` only when a GPU is present (wrap `import cudf.pandas; cudf.pandas.install()` in a try/except executed before `import pandas`).
- Develop on the laptop with pandas 3.0.x and numpy 2.4.x, the same versions cuDF 26.10 will force at the hackathon, to avoid pandas 2 -> 3 behaviour surprises (pandas 3 string dtype / copy-on-write).
- PaySim (6.3M rows, about 470 MB CSV, about 11 columns) should fit comfortably in 23 GB RAM with pandas or polars (order of 1-3 GB in memory depending on string columns), and CPU `hist` training on 8 cores should take on the order of minutes, not hours. This is an engineering estimate, not a measured or sourced figure.
- For PyG on CPU, subsample the transaction graph (the GNN is the piece most likely to be slow without a GPU).

### Gaps
- No official benchmark found for XGBoost `hist` CPU time/memory on a 6.3M-row dataset; the estimates above are unsourced and should be measured on the laptop.
- No sourced figure for the cudf.pandas speed-up on a T4 for this workload.

## 5. Deployment at the hackathon when the GPU environment is unknown (Docker, pip fallback, sizes, offline strategy)

### Takeaway
Prepare both paths: RAPIDS Docker images (4.1-6.1 GB compressed, need Docker + NVIDIA Container Toolkit + host driver) and a pip install into a fresh venv (multi-GB of wheels: libcugraph-cu12 alone is 969 MB, libcudf-cu12 667 MB, torch 539 MB). On venue Wi-Fi these downloads are the main risk, so pre-download images and wheels for both CUDA 12 and CUDA 13.

### Cited Findings
- Docker prerequisites: Docker Engine + nvidia-container-toolkit; test with `docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark` — [RAPIDS install](https://docs.rapids.ai/install/)
- NVIDIA Container Toolkit requires the NVIDIA GPU driver already installed on the host (package-manager install recommended) — [NVIDIA Container Toolkit install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- Images are Ubuntu-based (CUDA 12.5+ images on Ubuntu 24.04), multi-arch (x86_64 and ARM); `base` starts in an ipython shell (append `/bin/bash` to get a shell); `notebooks` runs JupyterLab on port 8888 — [RAPIDS install](https://docs.rapids.ai/install/)
- Docker Hub tags for 26.10 (last updated 2026-10-28), compressed size amd64: `rapidsai/base:26.10-cuda13-py3.12` 4.16 GB, `...-cuda13-py3.13` 4.12 GB, `...-cuda13-py3.11` 4.19 GB, `...-cuda13-py3.14` 4.15 GB; `rapidsai/base:26.10-cuda12-py3.12` 5.93 GB, `...-cuda12-py3.13` 5.90 GB, `...-cuda12-py3.11` 5.96 GB, `...-cuda12-py3.14` 5.93 GB — [Docker Hub API rapidsai/base](https://hub.docker.com/v2/repositories/rapidsai/base/tags?page_size=100&name=26.10)
- `rapidsai/notebooks:26.10-cuda13-py3.12` 4.32 GB; `rapidsai/notebooks:26.10-cuda12-py3.12` 6.10 GB (amd64, compressed) — [Docker Hub API rapidsai/notebooks](https://hub.docker.com/v2/repositories/rapidsai/notebooks/tags?page_size=100&name=26.10)
- NGC hosts stable images only (`nvcr.io/nvidia/rapidsai/base`), Docker Hub hosts stable and nightly — [RAPIDS install](https://docs.rapids.ai/install/)
- Image contents: cuDF, cuML, cuGraph, nx-cugraph, cuCIM, RAFT, cuVS (PyTorch, PyG, XGBoost are not in that list) — [RAPIDS install](https://docs.rapids.ai/install/)
- Wheel sizes (x86_64): `libcudf-cu12` 26.10.2 = 666.8 MB, `libcudf-cu13` = 301.4 MB — [PyPI libcudf-cu12](https://pypi.org/pypi/libcudf-cu12/json), [PyPI libcudf-cu13](https://pypi.org/pypi/libcudf-cu13/json); `libcugraph-cu12` 26.10.0 = 969.1 MB — [PyPI libcugraph-cu12](https://pypi.org/pypi/libcugraph-cu12/json); `libcuml-cu12` = 99.1 MB — [PyPI libcuml-cu12](https://pypi.org/pypi/libcuml-cu12/json); `libraft-cu12` = 26.1 MB — [PyPI libraft-cu12](https://pypi.org/pypi/libraft-cu12/json); `cupy-cuda12x` 148.2 MB / `cupy-cuda13x` 74.1 MB — [PyPI cupy-cuda12x](https://pypi.org/pypi/cupy-cuda12x/json), [PyPI cupy-cuda13x](https://pypi.org/pypi/cupy-cuda13x/json); `torch` 2.15.0 up to 539.2 MB plus separate nvidia-* wheels (e.g. `nvidia-nccl-cu13` 206.6 MB) — [PyPI torch](https://pypi.org/pypi/torch/json), [PyPI nvidia-nccl-cu13](https://pypi.org/pypi/nvidia-nccl-cu13/json); `xgboost` 57.6 MB, `xgboost-cu12` 83.5 MB — [PyPI xgboost](https://pypi.org/pypi/xgboost/json), [PyPI xgboost-cu12](https://pypi.org/pypi/xgboost-cu12/json)
- pip wheels need NVRTC; inside custom containers use `nvidia/cuda` `devel` images — [RAPIDS install](https://docs.rapids.ai/install/)
- Conda troubleshooting: a driver older than the requested `cuda-version` produces a `__cuda` constraint conflict; override possible with `CONDA_OVERRIDE_CUDA` — [RAPIDS install](https://docs.rapids.ai/install/)

### Inferences
- CUDA 12 artefacts are markedly larger than CUDA 13 ones (base image 5.9 GB vs 4.2 GB; libcudf 667 MB vs 301 MB).
- A full pip install of cuDF + cuML + cuGraph + torch + xgboost is plausibly 3-6 GB of downloads per CUDA major once all `nvidia-*`/`lib*` wheels are counted (sum not computed exhaustively); at 10 Mbit/s that is roughly 40-80 minutes, so it must not be left to venue Wi-Fi.
- Offline kit to prepare on a USB/SSD before 25 Nov: (1) `docker pull` then `docker save` of `rapidsai/base:26.10-cuda13-py3.12` and `rapidsai/base:26.10-cuda12-py3.12`, plus a small derived image adding torch, torch_geometric, xgboost, shap, fastapi, streamlit; (2) two wheelhouses built with `pip download -d wheels_cu13 ...` and `pip download -d wheels_cu12 ...` using `--python-version 3.12 --platform manylinux_2_28_x86_64 --only-binary=:all:` and `--extra-index-url https://pypi.nvidia.com`, installable with `pip install --no-index --find-links`; (3) PaySim CSV and a Parquet copy; (4) a CPU-only requirements file as last resort. These are standard pip/docker features, not something a RAPIDS page prescribes.
- Decision tree on arrival: run `nvidia-smi` → driver >= 580: Set A / cuda13 image; driver 525-579: Set B / cuda12 image; no Docker or no container toolkit: venv + wheelhouse; no working GPU stack: CPU fallback with identical code (`device="cpu"`, pandas).
- If the provided GPUs are cloud notebooks (Colab/Kaggle-like), the preinstalled cuDF/cuML should be used as-is rather than reinstalled.

### Gaps
- Uncompressed on-disk size of the images and of a full venv, and real install durations: not measured.
- Total download size of the complete dependency closure for each set: not computed (only the largest wheels were read).
- Whether hackathon machines allow Docker/root, and their driver version: unknown until organisers answer; worth asking them explicitly (GPU model, driver version, OS, Docker + nvidia-container-toolkit availability, internet speed).

## 6. XGBoost for serving: CPU single-row inference, model format portability, GPU SHAP

### Takeaway
Train on GPU, save with `save_model("model.ubj")` or `.json`, and serve on CPU in FastAPI: the model format is device-independent and version-stable, prediction is thread-safe for tree models, and SHAP-style reasons come from `predict(..., pred_contribs=True)` on either CPU or GPU.

### Cited Findings
- "Since 2.1.0, the default model format for XGBoost is the UBJSON format"; JSON and UBJSON share the same structure; choose by file extension `.json` or `.ubj` in `booster.save_model(...)`; loading dispatches on the extension — [XGBoost model IO](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html)
- "We guarantee backward compatibility for models but not for memory snapshots"; pickle/joblib snapshots are not stable across XGBoost or Python versions and pickle is not secure → use `save_model`, not pickle — [XGBoost model IO](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html)
- Custom objective/metric functions are not saved in the model file — [XGBoost model IO](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html)
- GPU-trained models work on CPU-only machines and vice versa — [XGBoost GPU support](https://xgboost.readthedocs.io/en/stable/gpu/index.html)
- In-place prediction bypasses `DMatrix` construction, "which is slow and memory consuming", and accepts numpy arrays and scipy CSR among others; with the native interface and early stopping, `best_iteration` is not applied automatically in `Booster.predict` / `inplace_predict` (it is in the sklearn interface) — [XGBoost prediction](https://xgboost.readthedocs.io/en/stable/prediction.html)
- Thread safety: since 1.4 all prediction functions, including SHAP value computation and `inplace_predict`, are thread-safe for `gbtree`/`dart`; training or `set_params` concurrently with prediction on the same model is not safe — [XGBoost prediction](https://xgboost.readthedocs.io/en/stable/prediction.html)
- GPU SHAP: `booster.set_param({"device": "cuda:0"})`, `shap_values = booster.predict(dtrain, pred_contribs=True)`, interactions with `pred_interactions=True`; XGBoost uses an in-tree `QuadratureTreeSHAP` implementation "on both CPU and GPU" — [XGBoost GPU support](https://xgboost.readthedocs.io/en/stable/gpu/index.html), [GPU SHAP example](https://xgboost.readthedocs.io/en/stable/python/examples/gpu_tree_shap.html)
- `inplace_predict` is preferred over `predict` when data is already on GPU — [XGBoost GPU support](https://xgboost.readthedocs.io/en/stable/gpu/index.html)
- `xgboost-cpu` (5.8 MB) is enough for the serving container — [XGBoost install](https://xgboost.readthedocs.io/en/stable/install.html), [PyPI xgboost-cpu](https://pypi.org/pypi/xgboost-cpu/json)

### Inferences
- Serving design: load the Booster once at FastAPI startup, score each request with `inplace_predict` on a 1xN numpy array, and compute per-request reasons with `pred_contribs=True` on CPU (one row is cheap); reserve GPU SHAP for batch explanation of the full dataset.
- Since `pred_contribs` is native to XGBoost, the `shap` package is only needed for plots (it requires Python >= 3.12 and numpy >= 2).
- Keep the same xgboost major/minor (3.4.x) in training and serving environments to avoid surprises, although backward compatibility of model files is guaranteed.

### Gaps
- No official figure for single-row CPU inference latency was found; the expectation of sub-millisecond to a few milliseconds for a few hundred trees is unsourced and must be measured (e.g. `timeit` over 1,000 single-row `inplace_predict` calls).
- Whether `inplace_predict` supports `pred_contribs` directly (the docs say it "has limited features"); SHAP may need `Booster.predict` on a small `DMatrix`.

## 7. Does Python 3.14 (laptop system Python) work, or use 3.11/3.12 via uv/conda?

### Takeaway
By wheel metadata, Python 3.14 is supported by every package in the stack as of Nov 2026, so the Kali system Python is not a blocker in principle; but an isolated Python 3.12 (uv or conda/miniforge) is still the right choice. Python 3.11 is no longer viable (xgboost 3.4.1, shap 0.54.1 and numpy 2.5 require >= 3.12).

### Cited Findings
- RAPIDS 26.10 supports Python 3.11, 3.12, 3.13, 3.14 (selector, platform table, and `-py3.14` Docker tags); 26.12 nightly supports 3.12-3.14 — [RAPIDS install](https://docs.rapids.ai/install/), [RAPIDS platform support](https://docs.rapids.ai/platform-support/), [Docker Hub API rapidsai/base](https://hub.docker.com/v2/repositories/rapidsai/base/tags?page_size=100&name=26.10)
- cuDF wheels are `cp311-abi3` (one wheel for all Python >= 3.11) with classifiers 3.11-3.14; cuML and cuGraph wheels are also abi3 but their classifiers list only 3.11 and 3.12 — [PyPI cudf-cu12](https://pypi.org/pypi/cudf-cu12/json), [PyPI cuml-cu12](https://pypi.org/pypi/cuml-cu12/json), [PyPI cugraph-cu12](https://pypi.org/pypi/cugraph-cu12/json)
- torch 2.15.0: cp311-cp315 wheels, classifiers 3.11-3.15 — [PyPI torch](https://pypi.org/pypi/torch/json); torch 2.14.1+cu126: cp310-cp315 — [cu126 index](https://download.pytorch.org/whl/cu126/torch/)
- xgboost 3.4.1: requires_python >=3.12, classifiers 3.12-3.14, `py3-none` wheels — [PyPI xgboost](https://pypi.org/pypi/xgboost/json)
- torch-geometric 2.8.1: classifiers 3.10-3.14; `pyg_lib` 0.9.0 wheels are `cp310-abi3` — [PyPI torch-geometric](https://pypi.org/pypi/torch-geometric/json), [torch-2.14.0+cu132](https://data.pyg.org/whl/torch-2.14.0+cu132.html)
- shap 0.54.1: requires_python >=3.12, cp312-abi3 wheels — [PyPI shap](https://pypi.org/pypi/shap/json); scikit-learn 1.9.1: cp311-cp315 — [PyPI scikit-learn](https://pypi.org/pypi/scikit-learn/json); fastapi 0.165.0 and streamlit 1.67.0: classifiers 3.11-3.15 — [PyPI fastapi](https://pypi.org/pypi/fastapi/json), [PyPI streamlit](https://pypi.org/pypi/streamlit/json)
- numpy 2.5.5 requires_python >=3.12; pandas requires `numpy>=2.3.3` on Python >= 3.14; numba 0.64.0 has cp310-cp314 wheels; cupy 14.2.0 has cp310-cp314 wheels — [PyPI numpy](https://pypi.org/pypi/numpy/json), [PyPI pandas](https://pypi.org/pypi/pandas/json), [PyPI numba 0.64.0](https://pypi.org/pypi/numba/0.64.0/json), [PyPI cupy-cuda13x](https://pypi.org/pypi/cupy-cuda13x/json)

### Inferences
- Recommend Python 3.12 in a dedicated environment (e.g. `uv venv --python 3.12`, or miniforge for the conda route) rather than the system 3.14: Kali's system Python is externally managed, 3.12 is the common floor of the stack and still supported by the next RAPIDS release, and it matches a RAPIDS image tag (`26.10-cudaXX-py3.12`) so laptop, Colab/Kaggle and hackathon environments can be aligned.
- On Python 3.14 the numpy window for the RAPIDS env is narrow: pandas needs numpy >= 2.3.3 and numba 0.64 needs numpy < 2.5, so numpy must be 2.3.3-2.4.x. Resolvable, but tighter than on 3.12.
- The laptop cannot install RAPIDS in a useful way (no NVIDIA GPU); its environment should be the CPU subset: pandas 3.0.x, numpy 2.4.x, xgboost-cpu 3.4.1, torch 2.15.0 or 2.14.1 CPU build, torch_geometric 2.8.1, scikit-learn, shap, fastapi, uvicorn, streamlit.

### Gaps
- The Python version of the hackathon machines and of current Colab/Kaggle runtimes was not verified.
- No install was run on Python 3.14, so "works on 3.14" rests on wheel tags and classifiers only.
