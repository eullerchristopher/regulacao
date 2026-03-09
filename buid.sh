#!/usr/bin/env bash

# instalar Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

# instalar dependências
pip install -r requirements.txt

# rodar migrations e coletar static
python manage.py migrate
python manage.py collectstatic --noinput

