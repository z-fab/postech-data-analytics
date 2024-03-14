import g_hist_idade from "../assets/g_hist_idade.json";
import g_pie_sexo from "../assets/g_pie_sexo.json";
import g_bar_diagnostico from "../assets/g_bar_diagnostico.json";
import g_bar_domicilio from "../assets/g_bar_domicilio.json";
import g_bar_escola from "../assets/g_bar_escola.json";
import g_bar_etnico from "../assets/g_bar_etnico.json";
import g_bar_restricao from "../assets/g_bar_restricao.json";
import g_bar_sintoma from "../assets/g_bar_sintoma.json";
import g_bar_trabalho from "../assets/g_bar_trabalho.json";
import g_cruza_rede_teste from "../assets/g_cruza_rede_teste.json";
import g_cruza_teste_diagnostico from "../assets/g_cruza_teste_diagnostico.json";
import g_cruza_teste_restricao from "../assets/g_cruza_teste_restricao.json";
import g_cruza_teste_sintoma from "../assets/g_cruza_teste_sintoma.json";
import g_pie_rede from "../assets/g_pie_rede.json";
import g_pie_teste from "../assets/g_pie_teste.json";
import Plot from "react-plotly.js";
import { Frame } from "plotly.js";

export function Relatorio() {
   return (
      <div className="flex flex-col items-center justify-center mb-20">
         <section className="w-2/3 min-w-[500px] max-w-[800px] mt-10 text-format">
            <p>
               Este relatório destina-se a avaliar o comportamento da população
               brasileira durante a pandemia de COVID-19, utilizando dados
               fornecidos pela Pesquisa Nacional por Amostra de Domicílios
               (PNAD-COVID-19) do IBGE para os meses de Setembro, Outubro e
               Novembro de 2020. O objetivo é compreender melhor os padrões
               demográficos, socioeconômicos e de saúde que podem informar
               estratégias futuras de resposta a pandemias.
            </p>

            <h2>Demografia</h2>
            <Plot
               data={(g_hist_idade as unknown as Frame).data}
               layout={(g_hist_idade as unknown as Frame).layout}
            />
            <p>
               A distribuição de idade dos respondentes, ilustrada no Histograma
               de Idade, mostra uma ampla gama de idades de 0 a 111 anos, com
               uma distribuição semelhante entre homens e mulheres. A presença
               de idades avançadas sugere a possibilidade de outliers que podem
               requerer uma análise adicional. O Gráfico de Distribuição de Sexo
               confirma uma divisão quase igual entre homens (52%) e mulheres
               (48%), refletindo a diversidade de gênero na amostra.
            </p>
            <Plot
               data={(g_pie_sexo as unknown as Frame).data}
               layout={(g_pie_sexo as unknown as Frame).layout}
            />

            <p>
               Em relação à autoidentificação étnico-racial, a maioria dos
               respondentes se classifica como Parda (49%) e Branca (41,8%),
               enquanto as categorias Preta, Amarela e Indígena representam uma
               parcela menor, como é visto no Gráfico de Distribuição
               Étnico-Racial. Este dado pode ter implicações importantes em
               termos de equidade no acesso a recursos de saúde e em campanhas
               de conscientização.
            </p>

            <Plot
               data={(g_bar_etnico as unknown as Frame).data}
               layout={(g_bar_etnico as unknown as Frame).layout}
            />

            <h2>Educação, Situação Habitacional e Comportamento</h2>
            <p>
               O perfil educacional dos participantes, demonstrado no Gráfico de
               Distribuição de Escolaridade, revela que 33,8% dos respondentes
               possuem Ensino Fundamental incompleto, o que pode indicar
               limitações no acesso à informação e na compreensão das
               orientações de saúde pública.
            </p>
            <Plot
               data={(g_bar_escola as unknown as Frame).data}
               layout={(g_bar_escola as unknown as Frame).layout}
            />
            <p>
               Quanto à situação habitacional, evidenciada no Gráfico do Tipo de
               Domicílio, a maior parte dos respondentes (68,2%) reside em
               moradia própria e quitada, enquanto o restante se divide entre
               alugados, cedidos e outras condições. O Gráfico do Tipo de
               Trabalho mostra que, dos que trabalham, a maioria é empregada do
               setor privado (16,3%).
            </p>
            <Plot
               data={(g_bar_domicilio as unknown as Frame).data}
               layout={(g_bar_domicilio as unknown as Frame).layout}
            />
            <Plot
               data={(g_bar_trabalho as unknown as Frame).data}
               layout={(g_bar_trabalho as unknown as Frame).layout}
            />
            <p>
               A análise do comportamento adotado em resposta à pandemia mostra
               que a grande maioria tomou alguma forma de medida restritiva. O
               Gráfico de Restrição de Contato indica que 42,2% reduziram o
               contato, e 39,9% saíram de casa apenas em casos de necessidade,
               enquanto somente 4% não realizaram qualquer restrição.
            </p>
            <Plot
               data={(g_bar_restricao as unknown as Frame).data}
               layout={(g_bar_restricao as unknown as Frame).layout}
            />
            <h2>Saúde e COVID-19</h2>
            <p>
               Dos respondentes que buscaram atendimento médico, 80% utilizaram
               a rede pública, conforme mostrado no Gráfico de Atendimento
               Médico. Isso ressalta o papel crítico do sistema de saúde público
               durante a crise. Entre os sintomas relatados na última semana, a
               dor de cabeça foi o mais comum, afetando 42,2% dos indivíduos,
               conforme ilustrado no Gráfico de Sintomas.
            </p>
            <Plot
               data={(g_pie_rede as unknown as Frame).data}
               layout={(g_pie_rede as unknown as Frame).layout}
            />
            <Plot
               data={(g_bar_sintoma as unknown as Frame).data}
               layout={(g_bar_sintoma as unknown as Frame).layout}
            />
            <p>
               O histórico de saúde anterior à pandemia é um fator relevante. O
               Gráfico de Diagnósticos Anterior mostra que 63,2% dos
               respondentes tinham hipertensão, o que pode influenciar a
               vulnerabilidade à COVID-19 e a severidade dos casos.
            </p>
            <Plot
               data={(g_bar_diagnostico as unknown as Frame).data}
               layout={(g_bar_diagnostico as unknown as Frame).layout}
            />
            <p>
               Ademais, dos que realizaram testes para COVID-19 (11% da base de
               respondentes), houve uma taxa de positividade de 25%.
            </p>
            <Plot
               data={(g_pie_teste as unknown as Frame).data}
               layout={(g_pie_teste as unknown as Frame).layout}
            />

            <h2>Cruzamento de Variáveis</h2>
            <p>O cruzamento de dados revelou relações interessantes:</p>
            <p>
               Houve diferença significativa na proporção de resultados
               positivos entre as redes pública e privada, porém é importante
               contextualizar que a maioria dos atendimentos tenha ocorrido na
               rede pública.
            </p>
            <Plot
               data={(g_cruza_rede_teste as unknown as Frame).data}
               layout={(g_cruza_rede_teste as unknown as Frame).layout}
            />
            <p>
               A presença de comorbidades prévias não mostrou influência
               significativa nos resultados dos testes de COVID-19, indicando
               que diagnósticos prévios podem influenciar a progressão da doença
               mas não a chance de infecção.
            </p>
            <Plot
               data={(g_cruza_teste_diagnostico as unknown as Frame).data}
               layout={(g_cruza_teste_diagnostico as unknown as Frame).layout}
            />
            <p>
               A perda de olfato ou paladar emergiu como um sintoma altamente
               indicativo de um teste positivo, enquanto sintomas como nariz
               entupido não foram considerados fortes indicadores.
            </p>
            <Plot
               data={(g_cruza_teste_sintoma as unknown as Frame).data}
               layout={(g_cruza_teste_sintoma as unknown as Frame).layout}
            />
            <p>
               Curiosamente, as taxas de positividade foram similares entre
               aqueles que aderiram estritamente ao isolamento domiciliar e os
               que não adotaram medidas restritivas, indicando que o relato das
               pessoas não deve ser levado fortemente em consideração na hora de
               realizar uma triagem.
            </p>

            <Plot
               data={(g_cruza_teste_restricao as unknown as Frame).data}
               layout={(g_cruza_teste_restricao as unknown as Frame).layout}
            />
         </section>
      </div>
   );
}
