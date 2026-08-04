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

Pesquise e compare aparelhos de todas as fabricantes relevantes.

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

Nunca invente informações técnicas.

Baseie todas as respostas em especificações técnicas reais e engenharia física dos aparelhos.

Responda EXCLUSIVAMENTE no formato abaixo.

Não utilize Markdown.

Não utilize blocos de código.

Não escreva títulos.

Não escreva comentários.

Não escreva explicações antes ou depois da resposta.

Cada aparelho deve seguir EXATAMENTE este formato:

modelo:
compatibilidade:
tamanho_tela:
justificativa:

Cada campo deve obrigatoriamente ocupar uma linha separada.

Deixe exatamente uma linha em branco entre um aparelho e outro.

Nunca coloque dois campos na mesma linha.

O campo "compatibilidade" deve conter apenas um destes valores:
- Alta
- Média
- Baixa

O campo "tamanho_tela" deve informar apenas o tamanho da tela.
Exemplo:
6.5"

O campo "justificativa" deve conter uma explicação técnica curta e objetiva, baseada em dimensões, formato da tela, posição da câmera frontal e compatibilidade física da película.

Retorne no mínimo 5 e no máximo 15 aparelhos compatíveis.

Ordene sempre da maior compatibilidade para a menor.

Inclua apenas aparelhos que possuam compatibilidade estrutural real.

Caso existam mais de 15 aparelhos compatíveis, retorne apenas os 15 de maior compatibilidade.

Caso existam menos de 15 aparelhos compatíveis, retorne todos os compatíveis encontrados.

Nunca utilize aparelhos repetidos.

Nunca invente compatibilidades inexistentes.

Exemplo do formato esperado:

modelo: Samsung Galaxy A12 Nacho
compatibilidade: Alta
tamanho_tela: 6.5"
justificativa: Mesma estrutura física, dimensões frontais muito semelhantes, cantos equivalentes e notch em "V".

modelo: Samsung Galaxy M12
compatibilidade: Alta
tamanho_tela: 6.5"
justificativa: Estrutura frontal praticamente idêntica, compartilhando dimensões e posicionamento da câmera frontal.

Retorne somente a resposta exatamente nesse padrão.
"""