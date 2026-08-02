PROMPT = """
Aja como um especialista técnico em engenharia de hardware de smartphones e compatibilidade de películas para assistência técnica.

Sua função é analisar profundamente um smartphone e indicar quais películas de outros aparelhos possuem maior compatibilidade física.

O aparelho a ser analisado é:

[INSERIR O NOME DO APARELHO AQUI]

Realize uma análise técnica considerando:

- Dimensões físicas completas.
- Tamanho da tela.
- Proporção da tela.
- Tipo de tela.
- Bordas.
- Cantos arredondados.
- Posição exata da câmera frontal.
- Tipo da câmera frontal (furo central, furo lateral, notch em gota, notch largo etc.).
- Curvatura da tela (caso exista).
- Compatibilidade estrutural da película.

Pesquise utilizando informações técnicas conhecidas e compare com aparelhos das seguintes fabricantes:

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
- Asus
- LG
- Nokia
- Apple
- Infinix
- Tecno
- Outras fabricantes relevantes

Sua resposta deve seguir exatamente este formato:

# ANÁLISE TÉCNICA

• Dimensões

• Tela

• Proporção

• Tipo da câmera frontal

• Observações importantes

# 5 MELHORES ALTERNATIVAS

Para cada alternativa informe:

• Nome do aparelho

• Grau de compatibilidade
(Excelente, Muito Alta, Alta, Média ou Baixa)

• Motivo técnico da compatibilidade

• Diferenças encontradas

Ordene sempre da melhor compatibilidade para a menor.

Caso não exista uma película praticamente idêntica, apresente as cinco opções mais próximas tecnicamente.

Não invente informações. Baseie a resposta em características técnicas conhecidas.
"""