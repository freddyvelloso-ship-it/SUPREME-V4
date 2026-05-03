# SUPREME-V4
A behavioral metrology framework for quantifying occupational exposure to traumatic content  through passive telemetry and aversive load dosimetry.

SUPREME V4

Production Engineering Specification
Backend Telemetry & Exposure Analytics System


Março 2026

Stack Tecnológica
Backend: Python 3.11+  |  FastAPI  |  SQLAlchemy  |  Pydantic
Dados: NumPy  |  Pandas
Banco: PostgreSQL 15+
Async: Celery  |  Redis
Infra: Docker

 
Registro de Correções Aplicadas
Este documento é a versão integrada da especificação original do SUPREME V4 com todas as correções técnicas aplicadas diretamente no texto. Seções alteradas são sinalizadas com caixas azuis indicando a natureza da correção.

Ref	Correção	Seção	Criticidade
C1	Pipeline matemático IEO unificado	39, 61	Crítico
C2	Particionamento de events_raw	18	Alto
C3	Política de baseline recalibration	37.5	Alto
C4	Deduplicação + UNIQUE constraint	11, 18	Médio
C5	CHECK constraint psychometric_data	23	Médio
C6	Celery Dead Letter Queue	46, 52, 55	Médio
C7	Retenção events_raw: 180 dias → 18 meses	28	Médio

 
1.	System Overview
Nota de enquadramento científico
O SUPREME V4 é um instrumento de mensuração comportamental, não um sistema de gestão de performance ou monitoramento disciplinar. Sua função científica é análoga à dos dispositivos de registro contínuo utilizados na pesquisa experimental em Análise do Comportamento — como câmeras de caixa operante, acumuladores de taxa de resposta e sistemas de registro de latência — transpostos para o ambiente naturalístico da perícia forense digital.
Na pesquisa experimental clássica, o comportamento operante é mensurado por suas propriedades temporais e de frequência: taxa de resposta, latência de iniciação, padrão de distribuição ao longo da sessão e sensibilidade a mudanças nas contingências ambientais (Skinner, 1938; Ferster & Skinner, 1957). O SUPREME opera segundo a mesma lógica: os eventos capturados pelos logs dos sistemas forenses — abertura de arquivo, visualização de imagem, reprodução de vídeo, classificação de evidência — são tratados como topografias mensuráveis do comportamento operante do perito sob controle de contingências aversivas. A latência entre eventos, a frequência de interrupções e o padrão de retomada de tarefas são as propriedades comportamentais de interesse — não indicadores de eficiência operacional.
A variável independente do estudo — a Intensidade de Exposição Ocupacional (IEO) — é calculada pelo sistema a partir dessas topografias e de metadados institucionais de severidade do conteúdo. Ela não é uma métrica de produtividade nem um índice de risco operacional: é um parâmetro ambiental que operacionaliza a magnitude cumulativa da estimulação aversiva à qual o perito está exposto em cada janela temporal, funcionando como Operação Estabelecedora no modelo analítico-comportamental adotado neste estudo.
As seções técnicas que seguem descrevem a arquitetura de implementação necessária para que essa mensuração ocorra de forma válida, confiável e eticamente governada no ambiente institucional da perícia forense digital. Os critérios de design — pseudonimização, acesso somente-leitura, separação entre dados operacionais e psicométricos, ausência de devolutiva individual — derivam diretamente dos requisitos científicos e éticos do protocolo de pesquisa, não de padrões genéricos de engenharia de softw
SUPREME V4 é um sistema backend de telemetria comportamental projetado para quantificar a Intensidade de Exposição Ocupacional (IEO) a partir de logs operacionais gerados durante a análise de material investigativo sensível em ambientes de perícia digital.
O sistema transforma eventos operacionais (ex.: visualização de imagem, reprodução de vídeo, classificação de evidência) em métricas comportamentais estruturadas que permitem:
•	medir carga de exposição ocupacional
•	monitorar evolução longitudinal da exposição
•	detectar padrões de risco psicológico associados à exposição cumulativa

O sistema é projetado para funcionar como backend analítico independente, capaz de ingerir dados provenientes de múltiplas ferramentas forenses e produzir métricas padronizadas acessíveis via API.

2. System Objectives

2.1 Quantificação de Exposição
Converter eventos operacionais em métricas quantitativas de exposição.
2.2 Modelagem Longitudinal
Construir séries temporais que permitam acompanhar a evolução da exposição ocupacional.
2.3 Detecção de Risco
Detectar padrões anormais de exposição associados a aumento de risco psicossocial.
2.4 Telemetria Comportamental
Permitir análise comportamental baseada em logs operacionais sem necessidade de intervenção direta no trabalho do perito.

3. System Context (C4 Level 1)
Actors
Forensic Analyst — usuário humano que opera ferramentas de análise forense.
Forensic Tools — Griffeye, Cellebrite e outras plataformas de análise digital que geram logs operacionais.
SUPREME Backend — responsável por ingestão, processamento, cálculo de métricas e análise longitudinal.
Analytics Client — aplicação que consulta os resultados analíticos via API.

Fluxo de contexto: Forensic Analyst → Forensic Tools → SUPREME Backend → PostgreSQL → Analytics Client

4. Container Architecture (C4 Level 2)
O sistema é dividido em containers lógicos.
Container	Responsabilidade	Tecnologia
4.1 API Service	Ingestão de eventos, consulta de métricas e IEO	FastAPI
4.2 Event Processing Engine	Validação, parsing e normalização de dados	Python / Pydantic
4.3 Session Builder	Agrupamento de eventos em sessões de atividade	Python
4.4 Metrics Engine	Cálculo de métricas comportamentais por janela	Python / NumPy
4.5 IEO Engine	Cálculo do índice de exposição ocupacional	Python / Pandas
4.6 Risk Detection Engine	Detecção de padrões de exposição críticos	Python
4.7 Database	Armazenamento persistente de eventos, sessões, métricas	PostgreSQL 15+

5. Data Flow
Read-Only Extraction Constraint
A coleta de logs das ferramentas forenses deve ocorrer EXCLUSIVAMENTE em modo leitura, utilizando: conexão read-only; journal_mode=WAL quando aplicável; acesso sem alteração de metadados. Essa restrição garante que o SUPREME opere apenas como camada analítica e não interfira na integridade dos dados periciais originais.

Pipeline de fluxo de dados:
•	Forensic Tool Logs
•	Event Ingestion API
•	Event Validation
•	Event Normalization
•	Session Builder
•	Metrics Engine
•	IEO Calculation Engine
•	Risk Detection Engine
•	PostgreSQL Storage
•	Analytics API

6. Technology Stack
Camada	Tecnologias
Backend	Python 3.11+, FastAPI, SQLAlchemy, Pydantic
Data Processing	NumPy, Pandas
Database	PostgreSQL 15+
Background Processing	Celery, Redis
Containerization	Docker
Observability	Prometheus, structured logs JSON
Security	TLS 1.3, AES-256, RBAC, JWT

7. Event Data Contract
Todos os eventos ingeridos devem obedecer ao seguinte schema JSON:
{
  "timestamp":        "ISO8601 UTC",
  "event_type":       "file_open | image_view | video_play | classification_event",
  "media_type":       "image | video | preview",
  "severity":         1,
  "duration_seconds": 4.5,
  "user_identifier":  "string",
  "source_tool":      "griffeye | cellebrite"
}

8. Event Type Definitions
Tipo	Descrição
file_open	Abertura de arquivo para análise
image_view	Visualização de imagem
video_play	Reprodução de vídeo
classification_event	Classificação/etiquetagem de evidência

9. Media Type Definitions
Tipo	Peso de intensidade
image	1.0
video	1.5
preview	0.5

10. Severity Scale
A severidade representa a intensidade do conteúdo analisado, mapeada na escala COPINE:
Nível	Descrição	Peso COPINE
1	Very low — non erotic / contextual	0.5
2	Low — nudity / non sexual	0.8
3	Moderate — explicit sexual context	1.0
4	High — severe sexual activity	1.3
5	Extreme — extreme abuse	1.6

11. Event Validation Rules
Eventos devem ser rejeitados se:
•	timestamp inválido (não-ISO8601 ou fora do período do estudo)
•	severity fora do intervalo [1, 5]
•	duration_seconds < 0
•	user_identifier vazio
•	event_hash duplicado (ver seção 18 — C4)

✎ CORRECAO APLICADA — C4 — Deduplicação por event_hash
O critério de duplicata é formalizado pelo campo event_hash, calculado como SHA256 dos campos funcionais do evento. Eventos com event_hash já presente na tabela são silenciosamente descartados via INSERT ... ON CONFLICT DO NOTHING, sem erro para o cliente.
def compute_event_hash(event):
    key = {k: event[k] for k in ['id_hash','timestamp','event_type',
                                   'media_type','severity','source_tool']}
    key['duration_seconds'] = round(event['duration_seconds'], 1)
    return hashlib.sha256(json.dumps(key,sort_keys=True).encode()).hexdigest()

12. Event Normalization
Antes do processamento, todos os eventos são normalizados. Campos obrigatórios: timestamp, event_type, media_type, severity, duration_seconds, user_identifier. Eventos com campos faltantes são descartados e registrados em system_health_logs.

13. Identity Pseudonymization
Identidades reais NUNCA são armazenadas no banco analítico.
Algoritmo
id_hash = SHA256(user_identifier + SALT_STRUCTURAL)

Salt Rules — Custódia obrigatória
•	O Salt estrutural é armazenado EXCLUSIVAMENTE em cofre criptográfico offline sob custódia do pesquisador principal.
•	O Salt NÃO é rotacionado durante o estudo.
•	O Salt NÃO é incluído em backups automatizados.
•	O Salt NÃO é armazenado em infraestrutura de produção.
•	A perda do Salt torna impossível a vinculação da série temporal histórica.

14. Session Engine
Eventos são agrupados em sessões de atividade com base em intervalos temporais.
Algoritmo de sessão
Eventos ordenados por timestamp
delta = timestamp[i] - timestamp[i-1]
delta ≤ 300s  →  mesma sessão
delta > 300s  →  nova sessão

Restrições
Parâmetro	Valor	Justificativa
min_session_duration	5 segundos	Filtra cliques acidentais
max_session_duration	12 horas	Filtra sessões esquecidas abertas
gap_threshold	300 segundos	Inatividade que delimita sessões

14.1 Event Latency Measurement
A latência entre eventos consecutivos do mesmo usuário é calculada via SQL VIEW:
CREATE VIEW event_latency AS
SELECT id_hash, timestamp,
       timestamp - LAG(timestamp)
       OVER (PARTITION BY id_hash ORDER BY timestamp) AS delta_t
FROM events_raw;
Esta métrica permite identificar pausas comportamentais anormais durante a análise de evidências.

15. Database Overview
O banco PostgreSQL 15+ armazena: eventos operacionais brutos, sessões comportamentais, métricas agregadas, índices de exposição, parâmetros de baseline, dados psicométricos, eventos críticos e logs operacionais.

16. Database Design Principles
Princípio	Descrição
16.1 Normalização	Estrutura normalizada até 3NF
16.2 Separação de camadas	Raw Telemetry / Processed Behavioral Data / Analytical Outputs
16.3 Imutabilidade de eventos	Eventos ingeridos não são alterados após armazenamento (append-only)
16.4 Indexação otimizada	Índices por usuário, por tempo e por janela temporal
16.5 Particionamento (C2)	events_raw particionada por range mensal (adicionado — ver seção 18)

17. Database Schema Overview
Tabela	Camada	Descrição
events_raw	Raw Telemetry	Eventos operacionais brutos ingeridos
sessions	Processed	Sessões comportamentais derivadas
window_metrics	Processed	Métricas agregadas por janela de 14 dias
ieo_logs	Analytical	Índice IEO calculado por janela
baseline_parameters	Analytical	Parâmetros de baseline individual
psychometric_data	Analytical	Resultados de instrumentos psicométricos
critical_load_flags	Analytical	Flags de exposição crítica
system_health_logs	Operations	Logs de funcionamento do pipeline

18. Table: events_raw
Tabela responsável por armazenar eventos operacionais ingeridos do sistema forense.
✎ CORRECAO APLICADA — C2 — Particionamento mensal + C4 — event_hash UNIQUE
Schema corrigido com particionamento RANGE por timestamp e campo event_hash para deduplicação.

CREATE TABLE events_raw (
    event_id         BIGSERIAL,
    id_hash          TEXT          NOT NULL,
    timestamp        TIMESTAMPTZ   NOT NULL,
    event_type       TEXT          NOT NULL,
    media_type       TEXT          NOT NULL,
    severity         INTEGER       NOT NULL
                     CHECK (severity BETWEEN 1 AND 5),
    duration_seconds FLOAT,
    source_tool      TEXT,
    event_hash       TEXT          NOT NULL,  -- C4: hash deduplicação
    created_at       TIMESTAMPTZ   DEFAULT NOW()
) PARTITION BY RANGE (timestamp);          -- C2: particionamento

-- Partições mensais (exemplo — gerar para cada mês do estudo)
CREATE TABLE events_raw_2026_01 PARTITION OF events_raw
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_raw_2026_02 PARTITION OF events_raw
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- [repetir para cada mês]

-- Constraint de deduplicação (C4)
ALTER TABLE events_raw ADD CONSTRAINT uq_event_hash UNIQUE (event_hash);

-- Índices (herdados por todas as partições no PG 15+)
CREATE INDEX idx_events_user      ON events_raw (id_hash);
CREATE INDEX idx_events_timestamp ON events_raw (timestamp);
CREATE INDEX idx_events_user_time ON events_raw (id_hash, timestamp);

Script de manutenção mensal (pg_cron)
DO $$ DECLARE
    next_month DATE := date_trunc('month', NOW() + INTERVAL '1 month');
    tbl TEXT := 'events_raw_' || to_char(next_month, 'YYYY_MM');
BEGIN
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF events_raw
         FOR VALUES FROM (%L) TO (%L)',
        tbl, next_month, next_month + INTERVAL '1 month');
END $$;

19. Table: sessions
CREATE TABLE sessions (
    session_id       UUID        PRIMARY KEY,
    id_hash          TEXT        NOT NULL,
    session_start    TIMESTAMP   NOT NULL,
    session_end      TIMESTAMP   NOT NULL,
    duration_minutes FLOAT,
    event_count      INTEGER,
    created_at       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_sessions_user  ON sessions (id_hash);
CREATE INDEX idx_sessions_start ON sessions (session_start);

20. Table: window_metrics
CREATE TABLE window_metrics (
    id_hash      TEXT    NOT NULL,
    window_start DATE    NOT NULL,
    T_minutes    FLOAT,
    E_events     INTEGER,
    V_volume     FLOAT,
    D_density    FLOAT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_hash, window_start)
);
CREATE INDEX idx_window_user ON window_metrics (id_hash);

21. Table: ieo_logs
CREATE TABLE ieo_logs (
    id_hash      TEXT    NOT NULL,
    window_start DATE    NOT NULL,
    ieo_score    FLOAT,
    ieo_linear   FLOAT,
    ieo_sat      FLOAT,
    z_T          FLOAT,
    z_E          FLOAT,
    z_V          FLOAT,
    z_D          FLOAT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_hash, window_start)
);

22. Table: baseline_parameters
✎ CORRECAO APLICADA — C3 — Campos adicionados para controle de baseline
Adicionados: baseline_version, baseline_frozen_at, baseline_status e recalibration_justification para suportar a política de congelamento e recalibração controlada.

CREATE TABLE baseline_parameters (
    id_hash                     TEXT PRIMARY KEY,
    mean_T                      FLOAT,
    sd_T                        FLOAT,
    mean_E                      FLOAT,
    sd_E                        FLOAT,
    mean_V                      FLOAT,
    sd_V                        FLOAT,
    mean_D                      FLOAT,
    sd_D                        FLOAT,
    baseline_window_count       INTEGER,
    baseline_last_update        TIMESTAMP,
    baseline_version            INTEGER     DEFAULT 1,        -- C3
    baseline_frozen_at          TIMESTAMPTZ,                  -- C3
    baseline_status             TEXT CHECK (baseline_status   -- C3
                                IN ('active','archived')),
    recalibration_justification TEXT                          -- C3
);

23. Table: psychometric_data
✎ CORRECAO APLICADA — C5 — Tipo ENUM para instrumento + CHECK em score
Campo instrument alterado de TEXT para o tipo psychometric_instrument (ENUM). Score limitado ao intervalo [0, 100]. Adicionados campos window_ref e dq_flag para rastreabilidade.

CREATE TYPE psychometric_instrument AS ENUM (
    'SRQ20', 'DASS21', 'OLBI', 'PANAS_SHORT'
);

CREATE TABLE psychometric_data (
    record_id   BIGSERIAL                PRIMARY KEY,
    id_hash     TEXT                     NOT NULL,
    instrument  psychometric_instrument  NOT NULL,  -- C5: ENUM
    score       FLOAT                    NOT NULL
                CHECK (score >= 0 AND score <= 100),-- C5: range
    timestamp   DATE                     NOT NULL,
    window_ref  DATE,   -- janela quinzenal de referência
    dq_flag     FLOAT   -- DQ da janela correspondente
);

24. Table: critical_load_flags
CREATE TABLE critical_load_flags (
    flag_id              BIGSERIAL  PRIMARY KEY,
    id_hash              TEXT       NOT NULL,
    timestamp            DATE       NOT NULL,
    ieo_value            FLOAT,
    psychometric_change  FLOAT,
    flag_confirmed       BOOLEAN    DEFAULT FALSE
);

25. Table: system_health_logs
CREATE TABLE system_health_logs (
    log_id          BIGSERIAL  PRIMARY KEY,
    timestamp       TIMESTAMP,
    pipeline_stage  TEXT,
    status          TEXT,
    error_message   TEXT,
    id_hash         TEXT,       -- referência ao usuário afetado
    window_start    DATE        -- janela afetada (se aplicável)
);

26–27. Relationship Model e Data Lifecycle
Fluxo de dados no banco
events_raw  →  sessions  →  window_metrics  →  ieo_logs
psychometric_data  +  ieo_logs  →  critical_load_flags

28. Data Retention Policy
✎ CORRECAO APLICADA — C7 — events_raw: 180 dias → 18 meses
Retenção original de 180 dias impossibilitaria reprocessamento na segunda metade do estudo (12 meses). Corrigido para 18 meses (duração do estudo + 6 meses de margem de segurança).

Tabela	Retenção	Justificativa
events_raw	18 meses (C7)	Reprocessamento completo do estudo + margem
sessions	Permanente	Dados de referência do modelo longitudinal
window_metrics	Permanente	Alimentam o modelo inferencial MLM
ieo_logs	Permanente	Série temporal principal do estudo
psychometric_data	≥ 5 anos pós-publicação	Protocolo CEP — dados clínicos
critical_load_flags	≥ 5 anos pós-publicação	Protocolo CEP — dados clínicos
system_health_logs	90 dias	Logs operacionais

29. Database Security
Medida	Especificação
Encryption at rest	AES-256 em disco
Encryption in transit	TLS 1.3
Access control	RBAC — roles: admin, analytics_user, system_operator
Audit logs	Todos os acessos registrados em system_health_logs
Separação lógica	Dados operacionais isolados de dados psicométricos

30. Backup Strategy
•	Backup diário incremental
•	Backup completo semanal
•	Retenção de 90 dias
•	Salt estrutural: backup offline manual, custódia exclusiva do pesquisador principal

31. Analytics Pipeline Overview
O pipeline analítico transforma eventos operacionais em indicadores de exposição, executado sequencialmente:
•	events_raw
•	sessions
•	behavioral metrics
•	window aggregation
•	IEO computation (pipeline unificado — ver seção 39/61)
•	risk detection

32. Session Metrics Extraction
Para cada sessão registrada, o sistema calcula: session_duration_minutes, session_event_count, session_volume.

33. Behavioral Metrics (Janela de 14 dias)
Variável	Definição	Unidade
T	Soma total de minutos de sessão na janela	minutos
E	Total de eventos válidos na janela	contagem
V	Volume ponderado de exposição (Σ W_evento × duração)	adimensional
D	Densidade de eventos: E / T	eventos/min

33.1 Exposure Time (T)
T = soma da duração de todas as sessões dentro da janela (minutos)
33.2 Event Count (E)
E = total de eventos válidos: image_view, video_play, classification_event, file_open
33.3 Exposure Volume (V)
Volume ponderado calculado a partir dos pesos de severidade (COPINE) e tipo de mídia — ver seção 34.

34. Exposure Weight Model
Cada evento possui peso: W_k = severity_weight × media_weight
34.1 Severity Weights (escala COPINE)
Severidade COPINE	Peso
1	0.5
2	0.8
3	1.0
4	1.3
5	1.6

34.2 Media Weights (multiplicadores por tipo de mídia)
Tipo de mídia	Multiplicador
image	1.0
video	1.5
preview	0.5

34.3 Volume Calculation
W_k   = media_weight × severity_weight   [por evento]
V     = Σ W_k                             [volume total da janela]

35. Event Density
D = E / T
Onde E = número de eventos e T = tempo total em minutos. Mede a intensidade de exposição por unidade de tempo.

36. Window Metrics Structure
Cada janela de 14 dias gera um registro WindowMetrics com campos: id_hash, window_start, T_minutes, E_events, V_volume, D_density.

37. Baseline Engine
✎ CORRECAO APLICADA — C3 — Política de baseline corrigida
A especificação original permitia recalibração automática após 180 dias sem critério de qualidade, o que poderia contaminar o baseline com períodos de crise. A política foi reformulada.

37.1 Baseline Requirements
•	Mínimo de 4 janelas válidas (DQ ≥ 0.5 cada)
•	Nenhuma janela com critical_load_flag pode integrar o baseline
•	Calculado exclusivamente durante a fase inicial (primeiras 4 a 8 janelas)

37.2 Baseline Variables
Para cada variável T, E, V, D são calculados: mean_X e standard deviation sd_X.
37.3 Baseline Calculation
mean_X = mean(X_i)   onde X_i = valor da variável na janela i
sd_X   = std(X_i)

37.4 Baseline Storage
Baseline armazenado em baseline_parameters. Campos ampliados (ver seção 22).
37.5 Baseline Recalibration — Política Corrigida (C3)
Baseline é CONGELADO após a fase inicial
Recalibração explícita só é permitida quando todas as condições abaixo são satisfeitas simultaneamente:
•	Solicitação formal documentada pelo pesquisador principal
•	Ausência de critical_load_flag nas últimas 6 janelas consecutivas
•	DQ ≥ 0.5 nas últimas 6 janelas consecutivas
•	Intervalo mínimo de 180 dias desde o último baseline
•	Aprovação registrada em log de auditoria com justificativa

O baseline anterior não é apagado — é arquivado com baseline_status = 'archived' e baseline_version incrementado.

38. Standardization Engine
Cada métrica é transformada em z-score relativo ao baseline congelado do analista:
z_X = (X - mean_X_baseline) / sd_X_baseline
38.1 Z-score Formula
A fórmula padrão aplicada a cada variável, relativa ao baseline congelado do analista:
z_X = (X - mean_X_baseline) / sd_X_baseline
38.2 Variables Standardized
Variáveis padronizadas: z_T, z_E, z_V, z_D.

39 & 61. IEO Engine — Pipeline Matemático Unificado (incorpora cap. 61)
✎ CORRECAO APLICADA — C1 — Inconsistência entre cap. 39 e cap. 61 resolvida
O documento original definia IEO_window (cap. 61) e IEO_linear (cap. 39) sem especificar a relação entre eles. Esta seção unifica o pipeline completo em 5 etapas sequenciais. Nota: o capítulo 61 (Analytical Business Rules, seções 61.1 a 61.5) foi integralmente incorporado nesta seção — não existe mais como capítulo independente. Todo o conteúdo de 61.1 (definição conceitual), 61.2 (fórmula matemática), 61.3 (tabela COPINE), 61.4 (multiplicadores de mídia) e 61.5 (exemplo de cálculo) está distribuído nas Etapas 1 a 5 e no exemplo numérico abaixo.

Etapa 1 — Peso por evento (nível de evento)
W_evento = COPINE_weight × media_multiplier

Etapa 2 — Agregação por sessão
IEO_session    = Σ W_evento
IEO_window_raw = IEO_session / session_duration_minutes

Etapa 3 — Agregação por janela quinzenal (14 dias)
T = Σ session_duration_minutes
E = contagem total de eventos válidos
V = Σ (IEO_window_raw × session_duration_minutes)   [volume ponderado]
D = E / T

Etapa 4 — Padronização por baseline individual
z_T = (T - mean_T) / sd_T
z_E = (E - mean_E) / sd_E
z_V = (V - mean_V) / sd_V
z_D = (D - mean_D) / sd_D

Etapa 5 — Combinação linear, saturação e ajuste de densidade
IEO_linear = 0.5·z_T + 0.3·z_E + 0.2·z_V   [α > β > γ; α+β+γ = 1]
IEO_sat    = 1 / (1 + exp(-1·(IEO_linear - 1)))
IEO_final  = IEO_sat + 0.1·z_D               [δ ≤ 0.20]

Exemplo numérico integrado
Evento: COPINE=4, mídia=video, 30 eventos, sessão de 45 min:
W_evento       = 1.3 × 1.5 = 1.95
IEO_session    = 30 × 1.95 = 58.5
IEO_window_raw = 58.5 / 45 = 1.30
V (janela)     = 1.30 × 45 = 58.5
z_V (baseline mean=30, sd=10) = (58.5 - 30) / 10 = 2.85

40. Logistic Saturation
A função logística evita crescimento ilimitado do índice em cenários de exposição extrema. Parâmetros: k = 1, x0 = 1. Ver pipeline unificado na seção 39.

41. Density Adjustment
Ajuste por densidade: IEO_final = IEO_sat + δ·z_D, com δ = 0.1 e restrição δ ≤ 0.20. Ver pipeline unificado na seção 39.

42. IEO Output Structure
Cada cálculo gera um IEORecord com campos:
Campo	Tipo	Descrição
id_hash	TEXT	Identificador pseudonimizado
window_start	DATE	Início da janela quinzenal
IEO_score	FLOAT	IEO_final (valor final do índice)
IEO_linear	FLOAT	Combinação linear antes da saturação
IEO_sat	FLOAT	Índice após função logística
z_T	FLOAT	Z-score do tempo de exposição
z_E	FLOAT	Z-score do número de eventos
z_V	FLOAT	Z-score do volume ponderado
z_D	FLOAT	Z-score da densidade

43. Risk Detection Engine
O sistema identifica situações de exposição crítica quando AMBAS as condições são satisfeitas simultaneamente:
Condição de carga crítica
IEO_final > 1.5 × SD_baseline
E simultaneamente:
psychometric_change >= 1.0 × SD_baseline
Onde psychometric_change = score_t − baseline_score

44. Psychometric Change
Mudança psicométrica: score_t − baseline_score. Instrumentos suportados: SRQ20, DASS21, OLBI, PANAS_SHORT.

45. Critical Flag Creation
Quando o critério é satisfeito: (1) gerar flag; (2) registrar em critical_load_flags; (3) acionar protocolo de suporte clínico obrigatório.

46. Processing Pseudocode
✎ CORRECAO APLICADA — C6 — Tratamento de erro e DLQ incluídos no pseudocódigo

for each user:
    build_sessions(events_raw)
    compute_window_metrics()
    if baseline not defined:
        update_baseline()
    compute_z_scores()
    compute_IEO_linear()
    compute_IEO_sat()
    compute_IEO_final()
    check_risk_conditions()
    store_results()
    on_error:
        log_to_system_health_logs(stage, error)
        retry(max=3, delay=60s)
        on_max_retries: send_to_dead_letter_queue()

47. API Overview
Categoria	Endpoints	Descrição
Ingestion API	POST /events/ingest	Ingestão de eventos em lote
Analytics API	GET /metrics/{id_hash}	Métricas comportamentais por janela
Analytics API	GET /ieo/{id_hash}	Índice IEO calculado por janela
Analytics API	GET /risk-flags	Flags de exposição crítica
Operations API	GET /health	Status do sistema e filas

Base URL: https://supreme.api.local/v1 — Autenticação: Bearer Token (JWT)

48. Endpoint: POST /events/ingest
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{ "events": [
    { "timestamp": "2026-02-01T10:10:05Z",
      "event_type": "image_view", "media_type": "image",
      "severity": 3, "duration_seconds": 5,
      "user_identifier": "user_021", "source_tool": "griffeye" }
  ] }

Response 200: { "status": "success", "events_received": 1, "events_stored": 1 }
Response 422: { "error_code": "INVALID_EVENT_SCHEMA", "message": "..." }

49. Endpoint: GET /metrics/{id_hash}
Response: { "id_hash": "a8f1e7...", "windows": [
    { "window_start": "2026-01-01", "T_minutes": 430,
      "E_events": 2100, "V_volume": 1820, "D_density": 4.88 } ] }

50. Endpoint: GET /ieo/{id_hash}
Response: { "id_hash": "a8f1e7...", "windows": [
    { "window_start": "2026-01-01", "IEO_score": 1.23,
      "IEO_linear": 0.88, "IEO_sat": 0.71,
      "z_T": 0.65, "z_E": 0.42, "z_V": 0.33, "z_D": 0.55 } ] }

51. Endpoint: GET /risk-flags
Query params: start_date, end_date, id_hash
Response: { "flags": [
    { "id_hash": "a8f1e7...", "timestamp": "2026-03-01",
      "IEO_value": 1.92, "psychometric_change": 1.3 } ] }

52. Endpoint: GET /health
✎ CORRECAO APLICADA — C6 — Health check ampliado para expor dead letter queue

Response: {
  "status": "ok",
  "database": "connected",
  "queue_analytics_size": 0,
  "queue_dead_letter_size": 0,   // ALERTA se > 0
  "last_pipeline_run": "2026-03-23T10:00:00Z"
}

53. Data Validation Layer
Validação ocorre antes da persistência. Eventos inválidos são descartados e registrados em system_health_logs.
Regra	Detalhe
timestamp	Deve ser ISO8601 UTC válido
severity	Deve estar no intervalo [1, 5]
duration_seconds	Deve ser >= 0
event_type	Deve ser um dos tipos definidos na seção 8
media_type	Deve ser um dos tipos definidos na seção 9
event_hash	Não pode existir já na tabela (ON CONFLICT DO NOTHING)

54. Error Handling
Estrutura padrão de erro:
{ "error_code": "STRING",
  "message":    "Human readable message",
  "details":    {} }

Código	Significado
INVALID_EVENT_SCHEMA	Evento não passa na validação de schema
DUPLICATE_EVENT	event_hash já presente (ignorado silenciosamente)
DATABASE_ERROR	Falha na persistência
AUTHENTICATION_FAILED	JWT inválido ou expirado
INTERNAL_SERVER_ERROR	Erro não categorizado no pipeline

55. Observability
✎ CORRECAO APLICADA — C6 — Métrica supreme_dead_letter_queue_size adicionada

Logs estruturados (todos os serviços)
{ "timestamp": "", "service": "", "level": "", "message": "" }

Métricas Prometheus
Métrica	Tipo	Descrição
events_ingested_total	Counter	Total de eventos ingeridos com sucesso
events_validation_errors_total	Counter	Total de eventos rejeitados na validação
pipeline_execution_seconds	Histogram	Duração do pipeline por janela
ieo_computation_seconds	Histogram	Duração do cálculo IEO
api_request_latency	Histogram	Latência dos endpoints da API
supreme_dead_letter_queue_size	Gauge	Tamanho da DLQ — alerta se > 0 (C6)

56. Security Architecture
Medida	Especificação
Encryption at rest	AES-256
Encryption in transit	TLS 1.3
Access control	RBAC
Roles	admin, analytics_user, system_operator
Autenticação API	Bearer Token (JWT)

57. Infrastructure
Arquitetura recomendada: Load Balancer → FastAPI API → Celery Workers → PostgreSQL DB.

57.1 Deployment Target Hardware
Ambiente	CPU	RAM	Storage	OS
Mínimo	4 cores	16 GB	200 GB SSD	Linux
Ideal	8 cores	32 GB	1 TB SSD	Linux

58. Docker Deployment
Serviços: api, worker, redis, postgres.
version: '3'
services:
  api:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    depends_on: [postgres, redis]
  worker:
    build: .
    command: celery -A worker worker --queues=analytics,events
    depends_on: [redis, postgres]
  redis:
    image: redis:7
  postgres:
    image: postgres:15

58b. Celery — Dead Letter Queue (C6)
✎ CORRECAO APLICADA — C6 — Seção adicionada: política de retry e DLQ
Seção não existia na especificação original. Incluída para garantir rastreabilidade de falhas no pipeline longitudinal.

# celery_config.py
from kombu import Queue, Exchange
task_queues = (
    Queue('events',     Exchange('events'),     routing_key='events'),
    Queue('analytics',  Exchange('analytics'),  routing_key='analytics'),
    Queue('dead_letter',Exchange('dead_letter'),routing_key='dead_letter'),
)
task_acks_late             = True
task_reject_on_worker_lost = True
task_max_retries           = 3
task_default_retry_delay   = 60  # segundos

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_window(self, id_hash, window_start):
    try:
        _run_pipeline(id_hash, window_start)
    except Exception as exc:
        SystemHealthLog.create(stage='process_window',
                               status='retry', error=str(exc))
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            _send_to_dead_letter(id_hash, window_start, str(exc))
            SystemHealthLog.create(stage='process_window',
                                   status='dead_letter', error=str(exc))

59. Dataset Example
2026-02-01T10:10:05Z,image_view,image,3,5,user_021,griffeye
2026-02-01T10:10:12Z,image_view,image,2,3,user_021,griffeye
2026-02-01T10:11:01Z,video_play,video,4,12,user_021,griffeye

60. Test Scenarios
Teste	Entrada	Resultado esperado
Test 1 — Event Ingestion	100 eventos válidos	100 registros em events_raw
Test 2 — Session Builder	Eventos separados por 200s	Mesma sessão
Test 3 — Window Metrics	Eventos dentro de 14 dias	1 registro em window_metrics
Test 4 — IEO Computation	Baseline definido	Cálculo de IEO_score
Test 5 — Risk Detection	IEO_final > 1.5 SD + Δpsych ≥ 1 SD	Flag em critical_load_flags
Test 6 — Deduplication (C4)	Mesmo lote enviado 2x	1 registro (segundo ignorado)
Test 7 — DLQ (C6)	Pipeline falha 4x seguidas	Entry em dead_letter_queue + log

 
62. Integração com Ferramentas Forenses — Especificação de Mecanismo de Extração
Esta seção especifica como o SUPREME V4 recebe os logs das ferramentas forenses (Griffeye, Cellebrite e equivalentes). É a lacuna operacional crítica não coberta nas seções anteriores — sem este mecanismo definido, o sistema não tem como receber dados reais.
São propostas três modalidades de integração, ordenadas por preferência técnica. A escolha final depende das permissões de acesso ao ambiente forense institucional.

62.1 Comparativo das Modalidades
Modalidade	Descrição	Complexidade	Intrusão no ambiente forense	Recomendado para
M1 — Log File Watcher	Agente leve monitora pasta de export das ferramentas	Baixa	Mínima — apenas leitura de arquivos	Piloto de viabilidade (este estudo)
M2 — Database Polling	Consulta periódica read-only ao banco interno das ferramentas	Média	Baixa — acesso ao BD sem escrita	Ambiente com DBA disponível
M3 — API Webhook	Ferramentas disparam eventos em tempo real via HTTP	Alta	Nenhuma — push model	Implantação permanente futura

 
62.2 Modalidade M1 — Log File Watcher (recomendada para o piloto)
Por que M1 para o piloto?
Não requer instalação de software no servidor forense.
Não requer acesso ao banco interno das ferramentas.
Funciona com qualquer ferramenta que exporte logs em CSV ou JSON.
Reversível: remover o agente não deixa rastros no ambiente forense.
Aprovação institucional mais simples — é equivalente a 'ler uma pasta compartilhada'.

Arquitetura M1
O operador forense configura a ferramenta (Griffeye/Cellebrite) para exportar logs de auditoria em uma pasta local ou de rede. O agente SUPREME monitora essa pasta e ingere os arquivos novos.
Griffeye/Cellebrite  -->  pasta/export/  -->  Log Watcher  -->  SUPREME API

Especificação do agente (supreme-watcher)
# supreme_watcher.py
import time, csv, json, hashlib, requests, os
from pathlib import Path
from datetime import datetime, timezone

WATCH_DIR   = Path('/mnt/forensic_exports')   # configurável por instituição
API_URL     = 'https://supreme.api.local/v1/events/ingest'
API_TOKEN   = os.environ['SUPREME_API_TOKEN']
STATE_FILE  = Path('/var/lib/supreme-watcher/processed.json')
POLL_SECS   = 60

def load_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def parse_griffeye_csv(path: Path) -> list[dict]:
    """Converte CSV de auditoria Griffeye para EventRecord SUPREME."""
    events = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            events.append({
                'timestamp':        row['Timestamp'],
                'event_type':       map_event_type(row['Action']),
                'media_type':       map_media_type(row['FileType']),
                'severity':         int(row.get('CopineLevel', 1)),
                'duration_seconds': float(row.get('ViewDuration', 0)),
                'user_identifier':  row['UserId'],
                'source_tool':      'griffeye',
            })
    return events

def map_event_type(action: str) -> str:
    return {
        'open_file':    'file_open',
        'image_view':   'image_view',
        'play_video':   'video_play',
        'tag_evidence': 'classification_event',
    }.get(action, 'file_open')

def map_media_type(file_type: str) -> str:
    if file_type.lower() in ('jpg','jpeg','png','bmp','gif','tiff'): return 'image'
    if file_type.lower() in ('mp4','avi','mov','wmv','mkv'):         return 'video'
    return 'preview'

def ingest_batch(events: list[dict]):
    resp = requests.post(API_URL,
        json={'events': events},
        headers={'Authorization': f'Bearer {API_TOKEN}'},
        timeout=30)
    resp.raise_for_status()
    return resp.json()

def run():
    state = load_state()
    while True:
        for csv_file in sorted(WATCH_DIR.glob('*.csv')):
            file_id = f"{csv_file.name}:{csv_file.stat().st_mtime}"
            if file_id in state:
                continue  # já processado
            try:
                events = parse_griffeye_csv(csv_file)
                result = ingest_batch(events)
                state[file_id] = {'processed_at': datetime.now(timezone.utc).isoformat(),
                                  'events_stored': result['events_stored']}
                save_state(state)
            except Exception as e:
                print(f'ERRO ao processar {csv_file}: {e}')
        time.sleep(POLL_SECS)

if __name__ == '__main__':
    run()

Configuração no Griffeye
No Griffeye Analyze DI: Settings → Audit Log → Export Path → apontar para a pasta monitorada. Formato: CSV. Frequência: ao fechar sessão ou a cada N minutos (configurável).

Configuração no Cellebrite UFED
No Cellebrite Physical Analyzer: File → Export → Activity Log → apontar para pasta compartilhada. Formato: CSV ou JSON. O campo UserId deve ser configurado com o identificador funcional do perito (não nome real).

Mapeamento obrigatório — Griffeye → SUPREME
Campo Griffeye	Campo SUPREME	Transformação
Timestamp	timestamp	Converter para ISO8601 UTC
Action	event_type	map_event_type() — ver Appendix A
FileType	media_type	map_media_type()
CopineLevel	severity	Integer [1–5]; default 1 se ausente
ViewDuration	duration_seconds	Float; default 0 se ausente
UserId	user_identifier	Pseudonimizado pelo watcher antes do envio

Mapeamento obrigatório — Cellebrite → SUPREME
Campo Cellebrite	Campo SUPREME	Transformação
EventTime	timestamp	Converter para ISO8601 UTC
EventType	event_type	map_event_type() — ver Appendix A
MediaCategory	media_type	map_media_type()
SeverityScore	severity	Integer [1–5]; default 1 se ausente
Duration	duration_seconds	Float em segundos; default 0
ExaminerID	user_identifier	Pseudonimizado pelo watcher

 
62.3 Modalidade M2 — Database Polling (alternativa para ambientes com DBA)
Quando o ambiente forense permite acesso read-only ao banco interno da ferramenta, o SUPREME pode consultar diretamente as tabelas de auditoria via SQL periódico, eliminando a dependência de exports manuais.

Requisitos
●	Usuário de banco com permissão SELECT apenas nas tabelas de auditoria.
●	Acesso de rede entre o servidor SUPREME e o servidor do banco forense.
●	Aprovação do responsável pela custódia do banco forense.

Implementação (SQLAlchemy + Celery)
# supreme_db_poller.py
from sqlalchemy import create_engine, text
from celery import shared_task
import os

FORENSIC_DB = os.environ['FORENSIC_DB_URL']  # read-only connection string
engine = create_engine(FORENSIC_DB, execution_options={'readonly': True})

# Query para Griffeye (ajustar nomes de tabela/coluna conforme versão)
GRIFFEYE_QUERY = text('''
    SELECT timestamp, action, file_type, copine_level,
           view_duration, user_id
    FROM audit_log
    WHERE timestamp > :last_polled
    ORDER BY timestamp ASC
    LIMIT 1000
''')

@shared_task
def poll_forensic_db(last_polled: str):
    with engine.connect() as conn:
        rows = conn.execute(GRIFFEYE_QUERY, {'last_polled': last_polled})
        events = [map_row_to_event(r) for r in rows]
    if events:
        ingest_batch(events)

Restrição obrigatória — M2
A connection string do banco forense NUNCA é armazenada no banco do SUPREME.
Deve ser injetada exclusivamente via variável de ambiente no container.
O usuário de banco deve ter GRANT SELECT apenas — nunca INSERT, UPDATE ou DELETE.
Toda query deve incluir ORDER BY timestamp + LIMIT para evitar full table scans.

62.4 Modalidade M3 — API Webhook (para implantação permanente futura)
Neste modelo, a ferramenta forense envia eventos ao SUPREME em tempo real via HTTP POST sempre que um evento ocorre. Elimina polling e latência de export, mas requer que a ferramenta suporte webhooks outbound — recurso presente no Griffeye 22+ e configurável via plugin no Cellebrite.

Fluxo M3
Griffeye/Cellebrite  -->  HTTP POST  -->  SUPREME /events/ingest  -->  Pipeline

Configuração no Griffeye (webhook outbound)
Settings → Integrations → Webhooks → Add → URL: https://supreme.api.local/v1/events/ingest → Events: all audit events → Auth Header: Authorization: Bearer {token}.

Endpoint receptor (já existente — seção 48)
O endpoint POST /events/ingest já é compatível com M3 sem modificações. O payload enviado pela ferramenta deve ser mapeado para o EventRecord schema (ver Appendix A). Recomenda-se adicionar validação de IP de origem para aceitar apenas o servidor forense.

62.5 Requisitos de Segurança Comuns às Três Modalidades
Requisito	M1 File Watcher	M2 DB Polling	M3 Webhook
Autenticação com SUPREME API	Bearer JWT	Bearer JWT	Bearer JWT
Dados forenses originais acessados	Não (apenas exports)	Sim (read-only)	Não (push da ferramenta)
Pseudonimização antes do envio	No watcher (antes do POST)	No poller (antes do POST)	Na ferramenta ou no endpoint
Isolamento de rede recomendado	Pasta compartilhada isolada	VPN ou rede interna	HTTPS + IP whitelist
Aprovação CEP/institucional	Baixa barreira	Média barreira	Baixa barreira
Auditoria de acesso	STATE_FILE local	Logs de query no BD forense	Logs de webhook na ferramenta

62.6 Impacto no Índice de Qualidade de Dados (DQ)
O mecanismo de integração escolhido afeta diretamente o DQ das janelas quinzenais. O DQ é calculado como proporção de eventos válidos sobre o total esperado na janela. Falhas no pipeline de extração reduzem o DQ e podem suspender a inserção no modelo inferencial (DQ < 0.5 — ver seção 37).

Causa de DQ baixo	Modalidade afetada	Mitigação
Export manual não realizado no prazo	M1	Lembrete automático ao operador + checklist semanal
Pasta de export inacessível (rede)	M1	Retry com backoff + alerta no /health
Banco forense em manutenção	M2	Janela de manutenção registrada no diário institucional
Ferramenta forense offline	M3	Fila local na ferramenta com retry para o endpoint
Formato de log alterado por update	M1, M2	Plano de contingência: versionar parser + testar após updates

Recomendação para este estudo (piloto de 12 meses)
Usar M1 (Log File Watcher) como modalidade principal.
Configurar o Griffeye para exportar logs automaticamente ao fechar cada sessão de análise.
Configurar o Cellebrite para exportar o Activity Log ao final de cada extração.
Implantar o supreme-watcher como serviço systemd no servidor SUPREME, apontando para a pasta de export.
Manter diário institucional de eventos técnicos (updates, manutenções, mudanças de software) para cruzamento com janelas de DQ baixo.
Ao final do piloto, avaliar migração para M3 se a instituição optar por implantação permanente.

62.7 Appendix C — Checklist de Implantação do Watcher (M1)
#	Ação	Responsável	Status
1	Configurar pasta de export no Griffeye	Operador forense / TI	[ ]
2	Configurar pasta de export no Cellebrite	Operador forense / TI	[ ]
3	Instalar supreme-watcher no servidor SUPREME	Desenvolvedor SUPREME	[ ]
4	Configurar SUPREME_API_TOKEN como variável de ambiente	Pesquisador principal	[ ]
5	Testar com 10 eventos sintéticos e verificar events_raw	Desenvolvedor SUPREME	[ ]
6	Verificar DQ ≥ 0.5 após primeira semana real	Pesquisador principal	[ ]
7	Registrar no diário institucional: data de início da coleta	Pesquisador principal	[ ]
8	Confirmar que user_identifier está pseudonimizado antes do envio	Pesquisador principal	[ ]

 
Appendix A — Event Dictionary
Tool Event	SUPREME Event
open_file	file_open
image_view	image_view
play_video	video_play
tag_evidence	classification_event

Appendix B — Example Log Dataset
timestamp,event_type,media_type,severity,duration_seconds,user_identifier,source_tool
2026-02-01T10:10:05Z,image_view,image,3,5,user_021,griffeye
2026-02-01T10:10:12Z,image_view,image,2,3,user_021,griffeye
2026-02-01T10:11:01Z,video_play,video,4,12,user_021,griffeye
2026-02-01T10:12:22Z,classification_event,image,3,2,user_021,griffeye


SUPREME V4 — Production Engineering Specification — Versão Integrada com Correções Técnicas v1.0 — Março 2026
