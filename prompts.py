PROMPT = """
Aja como um especialista técnico em engenharia de hardware de smartphones e compatibilidade de películas para assistência técnica.

Sua função é identificar, com o máximo de precisão possível, quais películas de outros aparelhos podem ser utilizadas no aparelho informado.

O aparelho a ser analisado é:

[INSERIR O NOME DO APARELHO AQUI]

Analise detalhadamente:

- Dimensões físicas.
- Altura.
- Largura.
- Espessura.
- Tamanho da tela.
- Tipo de tela.
- Proporção da tela.
- Formato dos cantos.
- Espessura das bordas.
- Curvatura da tela (caso exista).
- Tipo da câmera frontal.
- Localização exata da câmera frontal.
- Formato do notch ou furo.
- Espaçamento entre câmera e bordas.
- Compatibilidade estrutural da película.

Pesquise e compare aparelhos de todas as fabricantes relevantes, incluindo:

- Samsung
- Motorola
- Xiaomi
- Redmi
- Poco
- Realme
- Oppo
- Vivo
- Huawei
- Honor
- Apple
- Asus
- LG
- Nokia
- Infinix
- Tecno
- Google Pixel
- OnePlus
- Sony
- Demais fabricantes relevantes
Utilize conhecimento técnico para encontrar as películas mais compatíveis existentes no mercado.

Considere:

- Dimensões exatas.
- Aproveitamento da área útil da película.
- Posição da câmera frontal.
- Curvatura dos cantos.
- Bordas.
- Compatibilidade física da película.
- Possibilidade de adaptação em bancada.

Nunca utilize apenas o tamanho da tela como critério.

Priorize sempre aparelhos que realmente permitam utilizar a película sem necessidade de cortes ou adaptações.

Caso não exista compatibilidade perfeita, apresente as alternativas estruturalmente mais próximas.

Responda exatamente neste formato:

# ANÁLISE TÉCNICA

• Dimensões

• Tela

• Proporção

• Tipo e posição da câmera frontal

• Observações técnicas

# 5 MELHORES PELÍCULAS COMPATÍVEIS

Para cada alternativa informe:

• Nome do aparelho

• Grau de compatibilidade
(Excelente, Muito Alta, Alta, Média ou Baixa)

• Justificativa técnica detalhada

• Diferenças em relação ao aparelho pesquisado

• Motivo pelo qual a película pode ser utilizada

Ordene sempre da maior compatibilidade para a menor.

Nunca invente informações técnicas.

Caso não exista uma compatibilidade perfeita, apresente as opções estruturalmente mais próximas encontradas no mercado.

Baseie a resposta em especificações técnicas reais e engenharia física dos aparelhos.
"""


