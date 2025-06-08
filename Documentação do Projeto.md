**Documentação do Projeto: Sistema de Gestão de Estoque**  

### **1. Visão Geral**  
**Tecnologia Utilizada:**  
- Python  
- FastAPI  
- MySQL  
- Uvicorn (servidor ASGI)  

**Descrição:** API robusta para gerenciamento completo de estoque, incluindo cadastro de produtos, categorias, fornecedores, clientes e movimentações (entradas/saídas).  

**Objetivo:**  
Automatizar o controle de estoque com:  
- Cadastro centralizado de produtos e categorias  
- Rastreamento preciso de movimentações  
- Relatórios em tempo real  
- Segurança e escalabilidade  

---

### **2. Descrição Detalhada do Projeto**  
**O que é o projeto?**  
Sistema desenvolvido para otimizar a gestão de estoque em empresas, oferecendo:  
- Controle de inventário em tempo real  
- Validação de transações (ex.: evitar saídas sem estoque)  
- Integração direta com banco de dados MySQL  

#### **2.1 Funcionalidades Principais**  
| Funcionalidade          | Descrição                                                                 |  
|-------------------------|---------------------------------------------------------------------------|  
| **Cadastro de Produtos** | Inclui nome, custo, preço, quantidade e vinculação a categorias           |  
| **Gestão de Categorias** | Organização hierárquica de produtos (ex.: Eletrônicos > Computadores)     |  
| **Movimentações**        | Registro de entradas/saídas com validação de estoque                      |  
| **Relatórios**           | Dados consolidados por produto/categoria (futuro: exportação em PDF/Excel)|  
| **Autenticação**         | (Futuro) Proteção de endpoints com JWT e níveis de acesso                 |  

#### **2.2 Arquitetura do Código**  
```plaintext
estoque_api/  
├── main.py               # Configuração da API e endpoints principais  
├── database.py           # Conexão com MySQL e sessões SQLAlchemy  
├── schemas.py            # Modelos Pydantic para validação de dados  
├── models/  
│   └── models.py         # Modelos SQLAlchemy (tabelas do banco)  
├── requirements.txt      # Dependências (FastAPI, SQLAlchemy, MySQL-connector)  
└── README.md             # Guia de instalação e uso  
```

---

### **3. Etapas de Entrega (Cronograma)**  
| Etapa         | Data      | Entregáveis                                  |  
|---------------|-----------|----------------------------------------------|  
| **Documentação**       | 16/05    | Especificação técnica e arquitetura          |  
| **API Básica**         | 30/05    | CRUD de produtos, categorias e movimentações |  
| **Relatórios**         | 18/06    | Endpoints para consultas analíticas          |  
| **Testes Finais**      | 18/07    | Validação de fluxos e correções              |  

---

### **4. Equipe**  
| Nome           | Responsabilidade                |  
|----------------|---------------------------------|  
| **Athiely Taiany**  | Backend (API e banco de dados)  |  
| **Anna Júlia**     | Documentação e testes           |  
| **Maria Eduarda**  | Frontend (futuro) e relatórios  |  