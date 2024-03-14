import persona_g1 from "../assets/persona_g1.png";
import persona_g2 from "../assets/persona_g2.png";
import persona_g3 from "../assets/persona_g3.png";

export function Cluster() {
   return (
      <div className="flex flex-col items-center justify-center mb-20">
         <section className="w-2/3 min-w-[500px] max-w-[800px] mt-10 text-format">
            <p>
               Com o objetivo de entender melhor o comportamento e os perfis de
               saúde da população durante a pandemia de COVID-19, realizamos uma
               clusterização dos dados da PNAD-COVID-19 do IBGE com foco nos
               respondentes que usaram Rede Privada de Saúde. Esta análise
               permitiu a identificação de três grupos distintos com
               características e comportamentos semelhantes e a criação de
               personas representativas para cada cluster.
            </p>

            <h2>Descrição dos Clusters e Personas</h2>
            <h3>Cluster 1: Os Precavidos</h3>
            <p>
               Maioritariamente composto por mulheres com um nível de educação
               mais baixo, que não trabalham e têm restrições de contato
               significativas, saíndo apenas para necessidades básicas. Uma
               propensão a doenças cardíacas ou hipertensão, mas sem sintomas
               perceptíveis de COVID-19.
            </p>
            <div className="bg-zinc-100 rounded-xl h-[300px] overflow-clip flex items-center justify-between mb-24">
               <img
                  className="object-cover h-full w-1/3"
                  src={persona_g1}
                  alt="Ana Carolina"
               />
               <div className="w-3/4 p-8 flex flex-col justify-between">
                  <h4>Ana Carolina</h4>
                  <p>
                     Ana tem 52 anos e uma formação educacional até o ensino
                     fundamental. Como dona de casa, ela cuida ativamente da sua
                     família e da casa, priorizando a segurança e a saúde de
                     todos. Apesar dos recursos limitados, Ana mantém uma rotina
                     disciplinada de prevenção.
                  </p>
                  <p>
                     Hipertensiva e sem sintomas de COVID-19, Ana está sempre
                     vigilante às condições de saúde, adotando medidas
                     preventivas consistentes.
                  </p>
               </div>
            </div>

            <h3>Cluster 2: Os Conscientes</h3>
            <p>
               Indivíduos com educação de nível superior, que adotaram
               restrições rigorosas de contato, permanecendo em casa durante a
               pandemia. Apresentaram sintomas como tosse e dor de cabeça e
               tiveram maior probabilidade de testar positivo para COVID-19.
            </p>
            <div className="bg-zinc-100 rounded-xl h-[300px] overflow-clip flex items-center justify-between mb-24">
               <img
                  className="object-cover h-full w-1/3"
                  src={persona_g2}
                  alt="Julia Moraes"
               />
               <div className="w-3/4 p-8 flex flex-col justify-between">
                  <h4>Julia Moraes</h4>
                  <p>
                     Julia, de 35 anos, é uma analista de sistemas que levou o
                     isolamento muito a sério. Ela adaptou seu estilo de vida e
                     trabalho para permanecer o máximo possível em casa.
                  </p>
                  <p>
                     Teve sintomas leves da doença e buscou serviços de saúde
                     privados, conseguindo se recuperar sem complicações
                     significativas.
                  </p>
               </div>
            </div>

            <h3>Cluster 3: Os Adaptáveis</h3>
            <p>
               Homens com formação superior completa, que trabalham
               principalmente no setor privado e adaptaram suas interações
               sociais para reduzir o contato sem se isolar completamente. Não
               relataram sintomas significativos e fizeram uso de serviços de
               ambulatório privado para check-ups.
            </p>
            <div className="bg-zinc-100 rounded-xl h-[300px] overflow-clip flex items-center justify-between mb-24">
               <img
                  className="object-cover h-full w-1/3"
                  src={persona_g3}
                  alt="Rodrigo Oliveira"
               />
               <div className="w-3/4 p-8 flex flex-col justify-between">
                  <h4>Rodrigo Oliveira</h4>
                  <p>
                     Rodrigo, aos 40 anos, é um gerente de projetos que
                     conseguiu manter um equilíbrio entre o trabalho presencial
                     e remoto. Ele se ajustou às recomendações de saúde com
                     flexibilidade, sem comprometer sua rotina profissional.
                  </p>
                  <p>
                     Não teve sintomas que indicassem uma infecção por COVID-19,
                     mas procurou serviços de saúde privados para garantir sua
                     saúde e a de seus colegas de trabalho.
                  </p>
               </div>
            </div>

            <h2>Análise e Aplicação dos Insights</h2>
            <p>
               As personas criadas a partir dos clusters nos oferecem uma visão
               clara de como diferentes segmentos da população reagiram e foram
               afetados durante a pandemia. Ana representa os vulneráveis e mais
               precavidos, que apesar da falta de recursos, adotaram medidas
               rígidas de prevenção. Julia simboliza os que, mesmo seguindo as
               diretrizes de saúde pública, foram infectados, evidenciando a
               necessidade de atenção mesmo em grupos de menor risco aparente.
               Rodrigo reflete a capacidade de adaptação sem negligenciar a
               saúde, um equilíbrio importante para a continuidade das
               atividades econômicas.
            </p>
            <p>
               Essas personas podem ajudar as autoridades de saúde e os
               planejadores de políticas públicas a desenhar intervenções mais
               direcionadas e eficazes. Entender esses perfis facilita a
               personalização de comunicações e estratégias de prevenção, bem
               como o direcionamento de recursos para onde são mais necessários.
            </p>
         </section>
      </div>
   );
}
