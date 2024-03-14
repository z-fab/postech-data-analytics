export function Processo() {
   return (
      <div className="flex flex-col items-center justify-center mb-20">
         <div className="w-2/3 min-w-[500px] max-w-[800px] mt-10 text-format">
            <p>
               O relatório a seguir descreve o processo de ETL (Extract,
               Transform, Load) realizado com os dados da PNAD-COVID-19 do IBGE,
               focando na análise do comportamento da população durante a
               pandemia da COVID-19 e o planejamento para potenciais surtos
               futuros.
            </p>

            <h2>1. Obtenção dos Microdados</h2>
            <p>
               Microdados são conjuntos de dados brutos e detalhados, coletados
               diretamente na fonte, antes de qualquer processamento ou análise.
               Para este projeto, os microdados da PNAD-COVID-19 referentes aos
               meses de Setembro, Outubro e Novembro de 2020 foram obtidos
               diretamente do site do IBGE.
            </p>

            <h2>2. Estruturação do Datalake</h2>
            <p>
               A estruturação dos dados foi feita para simular a organização de
               um datalake dividida em 3 camadas: Bronze, Silver e Gold
            </p>
            <div className="flex justify-around gap-5 text-center">
               <div className="p-5 bg-orange-100 rounded-lg flex-1">
                  <h3>Camada Bronze</h3>
                  <p>
                     A camada Bronze funcionou como o repositório inicial para
                     os dados brutos, armazenando os CSVs obtidos.
                  </p>
               </div>
               <div className="p-5 bg-gray-100 rounded-lg flex-1">
                  <h3>Camada Silver</h3>
                  <p>
                     Os CSVs foram consolidados em uma única tabela na camada
                     Silver após a verificação da consistência do esquema dos
                     dados.
                  </p>
               </div>
               <div className="p-5 bg-amber-100 rounded-lg flex-1">
                  <h3>Camada Gold</h3>
                  <p>
                     Na camada Gold, os dados foram enriquecidos e refinados
                     para análises mais específicas e avançadas.
                  </p>
               </div>
            </div>

            <h2>3. Análise Exploratória de Dados (EDA)</h2>
            <p>
               Realizamos análises exploratórias para entender melhor as
               características e padrões presentes nos dados e exploramos
               algumas hipóteses, relacionadas principalmente às variáveis de
               resultado do teste.
            </p>

            <h2>4. Modelo de Clusterização e Persona</h2>
            <p>
               Utilizamos a técnica de KMeans para segmentar os dados em grupos
               com características semelhantes. Em seguida para cada grupo
               identificado, criamos uma persona representativa, simplificando a
               interpretação dos resultados.
            </p>
         </div>
      </div>
   );
}
