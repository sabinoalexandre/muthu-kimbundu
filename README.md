# MUTHU — Tradutor de Português ↔ Kimbundu

**MUTHU** é uma aplicação bilingue de tradução concebida para traduzir palavras, expressões, frases, parágrafos e textos mais longos entre o português e o Kimbundu.

**Lema:** «Duas línguas. Uma conexão.»

---

## 1. Visão geral do projeto

O MUTHU tem como objetivo tornar a comunicação entre o português e o Kimbundu mais acessível, através de uma interface intuitiva, uma arquitetura modular e recursos linguísticos cuidadosamente geridos.

O projeto pretende também contribuir para a preservação, valorização e acessibilidade digital da língua Kimbundu.

A aplicação foi concebida para funcionar em computadores e dispositivos móveis, com especial atenção à experiência de utilização em smartphones Android.

## 2. Funcionalidades

- Interface responsiva, desenvolvida com KivyMD e concebida prioritariamente para dispositivos móveis.
- Navegação inferior entre os diferentes ecrãs da aplicação.
- Ecrãs com conteúdo deslizável, pesquisa em tempo real e mensagens informativas quando não existem resultados.
- Campos de texto adaptados à utilização do teclado.
- Tradução bidirecional:
  - Português → Kimbundu.
  - Kimbundu → Português.
- Tradução de palavras, expressões, frases, parágrafos e textos extensos.
- Dicionário bilingue com funcionalidade de pesquisa.
- Histórico de traduções com pesquisa, eliminação individual e limpeza completa.
- Sistema de favoritos para guardar traduções e expressões.
- Temas claro e escuro.
- Tipografia JetBrains Mono incluída no aplicativo para funcionar também sem instalação da fonte no dispositivo.
- Comunicação transparente sobre expressões não suportadas e limitações das traduções.
- Quando não existe uma correspondência no dicionário, o texto original é apresentado e identificado como não encontrado, em vez de apresentar uma tradução inventada ou uma mensagem de erro.
- Dicionário local inicial com palavras de fontes identificadas e expressões compostas documentadas.
- Carregamento inicial dos recursos lexicais para a tabela do dicionário SQLite.

## 3. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação principal. |
| Kivy | Framework para desenvolvimento da aplicação. |
| KivyMD | Componentes de interface baseados no Material Design. |
| SQLite | Base de dados local para armazenamento de informações. |
| Buildozer | Ferramenta para empacotamento da aplicação Android. |
| Pytest | Framework para execução de testes automatizados. |

### Ambiente de desenvolvimento

A interface foi concebida para uma visualização de 360 × 640 píxeis (proporção 9:16) em computadores, utilizando o tamanho nativo do ecrã em dispositivos móveis. A fonte JetBrains Mono é carregada de `assets/fonts/` em todas as plataformas; a licença SIL OFL 1.1 acompanha a fonte.

O empacotamento para Android é configurado através do Buildozer, permitindo gerar localmente um ficheiro APK de depuração.

A configuração fixa o Android NDK na versão 28c, recomendada pelo python-for-android usado pelo Buildozer.

---

## 4. Requisitos do sistema

### 4.1. Sistema operativo

Este guia considera o **Debian Linux** como ambiente principal de desenvolvimento.

Outros sistemas Linux podem ser utilizados, desde que disponibilizem as dependências necessárias.

### 4.2. Requisitos de software

- Debian 12 ou superior.
- Python 3.13 (conforme a configuração do projeto).
- pip.
- venv.
- Git.
- Kivy e KivyMD, de acordo com as versões definidas em `requirements.txt`.
- Ambiente gráfico funcional para executar a aplicação no computador.

Para a compilação Android, também são necessários Java, Buildozer, Cython e as ferramentas de desenvolvimento Android.

---

## 5. Instalação no Debian

### 5.1. Atualizar o sistema

Antes de começar, atualize os pacotes do sistema:

```bash
sudo apt update
sudo apt upgrade -y
```

### 5.2. Instalar as dependências do sistema

Instale o Python e as ferramentas necessárias:

```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    pkg-config
```

Para evitar problemas durante a instalação e execução de componentes gráficos do Kivy, instale também:

```bash
sudo apt install -y \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libmtdev-dev \
    libffi-dev \
    libssl-dev
```

### 5.3. Obter o projeto

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta do projeto:

```bash
cd MUTHU
```

Substitua `<URL_DO_REPOSITORIO>` pelo endereço real do repositório Git.

### 5.4. Instalar as dependências Python

O Debian utiliza o mecanismo PEP 668 para proteger o ambiente Python gerido pelo sistema.

Por esse motivo, **não é recomendado instalar as dependências do projeto diretamente no Python global através de `pip install`**.

O MUTHU utiliza um ambiente virtual próprio (`.venv`).

Execute:

```bash
make install
```

Este comando:

1. Cria o ambiente virtual `.venv`.
2. Atualiza o pip, setuptools e wheel.
3. Instala as dependências definidas em `requirements.txt`.

Não é necessário utilizar `sudo pip install`.

---

## 6. Executar a aplicação

Depois de concluir a instalação, execute:

```bash
make run
```

A aplicação será iniciada utilizando o Python do ambiente virtual.

Também é possível executar diretamente:

```bash
.venv/bin/python main.py
```

### 6.1. Ativar manualmente o ambiente virtual

Se pretender trabalhar diretamente no terminal com as dependências instaladas:

```bash
source .venv/bin/activate
```

Depois de ativar o ambiente virtual, poderá executar:

```bash
python main.py
```

Para sair do ambiente virtual:

```bash
deactivate
```

---

## 7. Configuração da aplicação

Copie o ficheiro de configuração de exemplo:

```bash
cp .env.example .env
```

Ajuste os valores conforme as necessidades do projeto.

### Variáveis disponíveis

| Variável | Descrição |
|---|---|
| `TRANSLATION_PROVIDER` | Estratégia inicial de tradução: `dictionary` ou `machine`. |
| `MUTHU_THEME` | Tema inicial da aplicação: `light` ou `dark`. |
| `MUTHU_DEFAULT_SOURCE` | Idioma de origem predefinido: `pt` ou `kimbundu`. |
| `MUTHU_DEFAULT_TARGET` | Idioma de destino predefinido: `pt` ou `kimbundu`. |

As credenciais de APIs externas estão reservadas para futuros serviços de tradução.

Atualmente, não é necessária nenhuma chave de API.

---

## 8. Compilação e instalação no Android

O Buildozer permite empacotar a aplicação Kivy num ficheiro APK, que pode ser instalado num dispositivo Android.

A compilação deve ser realizada num ambiente Linux ou macOS. No Windows, pode ser utilizado o WSL2.

### 8.1. Instalar as dependências do sistema

No Debian, instale as ferramentas necessárias:

```bash
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3-dev \
    build-essential \
    autoconf \
    automake \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses-dev \
    libffi-dev \
    libssl-dev \
    libltdl-dev
```

O Buildozer também necessita das ferramentas e componentes do Android SDK e NDK, que podem ser descarregados durante a primeira compilação.

Consulte a [documentação oficial de instalação do Buildozer](https://buildozer.readthedocs.io/en/latest/installation/) para verificar os requisitos específicos da versão utilizada.

### 8.2. Instalar o Buildozer

O projeto utiliza o ambiente virtual `.venv`.

O Buildozer está incluído em `requirements.txt` e é instalado por `make install`. Também pode instalá-lo manualmente nesse ambiente:

```bash
.venv/bin/python -m pip install --upgrade buildozer setuptools
```

Instale também a versão de Cython indicada para o processo de compilação:

```bash
.venv/bin/python -m pip install "cython==0.29.34"
```

### 8.3. Gerar o APK

Execute:

```bash
make app
```

Este comando executa:

```bash
.venv/bin/buildozer -v android debug
```

Na primeira compilação, o Buildozer descarrega o Android SDK, NDK e outras ferramentas necessárias.

Este processo pode demorar bastante, dependendo da velocidade da Internet e dos recursos do computador.

Quando a compilação terminar, o APK será gerado na pasta:

```text
bin/
```

### 8.4. Instalar a aplicação através de USB

No dispositivo Android:

1. Ative as opções de programador.
2. Ative a depuração USB.
3. Ligue o dispositivo ao computador.
4. Autorize a ligação USB, quando solicitado.

Execute:

```bash
.venv/bin/buildozer android deploy run
```

Este comando tenta instalar e executar a aplicação no dispositivo conectado.

### 8.5. Instalar o APK manualmente

Também é possível copiar o ficheiro APK da pasta `bin/` para o telemóvel.

Abra o ficheiro no dispositivo Android e autorize a instalação de aplicações provenientes dessa origem, caso seja solicitado.

**Nota:** O APK de depuração destina-se a testes e instalação direta. A publicação na Google Play exige uma versão de lançamento devidamente assinada.

Para mais informações, consulte o [Guia oficial do Buildozer](https://buildozer.readthedocs.io/en/latest/quickstart/).

---

## 9. Testes e qualidade do código

O projeto utiliza Pytest para executar testes automatizados.

Para executar todos os testes:

```bash
make test
```

Outros comandos disponíveis:

| Comando | Descrição |
|---|---|
| `make install` | Cria o ambiente virtual e instala as dependências. |
| `make run` | Executa a aplicação. |
| `make debug` | Inicia a aplicação no depurador Python. |
| `make test` | Executa os testes automatizados. |
| `make lint` | Verifica a qualidade e possíveis problemas no código. |
| `make lint-strict` | Executa verificações rigorosas com MyPy. |
| `make app` | Compila a aplicação Android. |
| `make clean` | Remove ficheiros e diretórios gerados durante o desenvolvimento. |
| `make re` | Limpa os ficheiros gerados e executa novamente a aplicação. |

### Verificação de qualidade

Para executar as verificações:

```bash
make lint
```

Para uma verificação mais rigorosa:

```bash
make lint-strict
```

### Limpeza do projeto

Para remover ficheiros temporários e resultados de compilação:

```bash
make clean
```

**Atenção:** O comando `make clean` também remove `bin/` e `.buildozer/`, caso estejam definidos dessa forma no Makefile. Isto elimina os APKs gerados e os ficheiros de compilação Android, podendo obrigar a descarregar novamente componentes na próxima compilação.

---

## 10. Estrutura do projeto

A aplicação segue uma arquitetura modular, separando a interface, a lógica de negócio, os serviços e o armazenamento de dados.

```text
MUTHU/
│
├── main.py
├── requirements.txt
├── README.md
├── Makefile
├── buildozer.spec
├── .gitignore
├── .env.example
│
├── assets/
│   └── fonts/
│       └── JetBrainsMono-Regular.ttf
│
├── src/
│   ├── ui/
│   ├── core/
│   ├── services/
│   ├── providers/
│   ├── database/
│   └── config/
│
├── data/
│   └── linguistic_resources/
│
├── tests/
│
└── .venv/
```

### Responsabilidade dos principais diretórios

| Diretório | Responsabilidade |
|---|---|
| `assets/` | Recursos visuais e outros elementos utilizados pela interface. |
| `src/ui/` | Ecrãs, componentes e elementos da interface gráfica. |
| `src/core/` | Lógica central e regras de funcionamento da aplicação. |
| `src/services/` | Serviços e operações disponibilizados à aplicação. |
| `src/providers/` | Implementações dos diferentes mecanismos de tradução. |
| `src/database/` | Gestão da base de dados e operações SQLite. |
| `src/config/` | Configurações e parâmetros da aplicação. |
| `data/` | Dados locais e recursos linguísticos. |
| `tests/` | Testes automatizados. |
| `.venv/` | Ambiente virtual Python e dependências instaladas. |

A estrutura apresentada representa a organização prevista do projeto. Os diretórios efetivamente existentes podem variar conforme a implementação.

---

## 11. Limitações da tradução

O MUTHU encontra-se numa fase inicial de desenvolvimento dos seus recursos linguísticos.

É importante compreender as seguintes limitações:

- Ainda não foi validado um serviço de tradução automática capaz de traduzir Kimbundu de forma suficientemente fiável.
- A implementação inicial utiliza um mecanismo de tradução baseado num dicionário local.
- A pesquisa de palavras no dicionário não equivale à tradução contextual de frases completas.
- Os resultados são identificados como consultas ao dicionário.
- As entradas linguísticas não verificadas são devidamente identificadas.
- Quando uma expressão não é encontrada, o texto original é preservado e apresentado com o estado de correspondência não encontrada.
- Traduções incertas nunca devem ser apresentadas como traduções confirmadas.

A prioridade é garantir a transparência e a fiabilidade dos resultados, evitando a apresentação de traduções inventadas.

---

## 12. Dados linguísticos e verificação

Os recursos linguísticos encontram-se organizados no diretório:

```text
data/
```

Incluindo:

```text
data/linguistic_resources/
```

Cada entrada do dicionário deve conter:

- Palavra ou expressão.
- Equivalente linguístico.
- Idioma de origem e de destino.
- Estado de verificação.
- Referência da fonte utilizada.

### Estados de verificação

| Estado | Significado |
|---|---|
| `verified` | Entrada verificada e validada. |
| `unverified` | Entrada ainda não validada. |

As contribuições da comunidade permanecem classificadas como não verificadas até serem analisadas por falantes de Kimbundu ou especialistas na língua.

A qualidade dos dados linguísticos é essencial para garantir a credibilidade do MUTHU.

---

## 13. Desenvolvimento e contribuição

O MUTHU segue uma arquitetura modular que procura manter uma separação clara entre:

- Apresentação e interface gráfica.
- Lógica de aplicação.
- Regras de negócio.
- Serviços.
- Fornecedores de tradução.
- Camada de persistência e armazenamento de dados.

Esta organização facilita a manutenção, os testes e a futura integração de novos mecanismos de tradução.

### Contribuições

São bem-vindas contribuições relacionadas com:

- Correção e validação de traduções.
- Ampliação do dicionário português–Kimbundu.
- Documentação de expressões e estruturas linguísticas.
- Melhorias na interface e experiência de utilização.
- Correção de erros e otimização do código.
- Testes e compatibilidade com diferentes dispositivos.

As contribuições linguísticas devem incluir referências às fontes e permanecer identificadas como não verificadas até à sua validação.

---

## 14. Trabalho futuro

O desenvolvimento do MUTHU poderá incluir:

- Integração de um modelo de tradução automática validado para português e Kimbundu.
- Expansão do dicionário bilingue.
- Validação linguística das palavras e expressões existentes.
- Colaboração com falantes nativos e especialistas em Kimbundu.
- Melhoria da tradução contextual de frases e textos extensos.
- Desenvolvimento e distribuição da aplicação Android.
- Possível integração de funcionalidades de reconhecimento e síntese de voz.
- Expansão dos recursos linguísticos para apoiar a preservação digital do Kimbundu.

---

## 15. Objetivo do projeto

O MUTHU não pretende ser apenas uma ferramenta de tradução.

Pretende ser uma iniciativa tecnológica que aproxima duas línguas, facilita a comunicação e contribui para a valorização e preservação do património linguístico angolano.

**MUTHU — Duas línguas. Uma conexão.**
