//import g_hist_idade from "../assets/g_hist_idade.json";
//import g_pie_sexo from "../assets/g_pie_sexo.json";
//import Plot from "react-plotly.js";
//import { Frame } from "plotly.js";

export function Contexto() {
   return (
      <div className="flex flex-col items-center justify-center mb-20">
         <div className="w-2/3 min-w-[500px] max-w-[800px] mt-10 text-format">
            <section>
               <p>
                  Imagine agora que você foi contratado(a) como Expert em Data
                  Analytics por um grande hospital para entender como foi o
                  comportamento da população na época da pandemia da COVID-19 e
                  quais indicadores seriam importantes para o planejamento, caso
                  haja um novo surto da doença.
               </p>
               <p>
                  A sua área observou que a utilização do estudo do PNAD-COVID
                  19 do IBGE seria uma ótima base para termos boas respostas ao
                  problema proposto, pois são dados confiáveis.
               </p>
            </section>

            <section>
               <h2>Sobre o projeto</h2>
               <p>
                  O Head de Dados pediu para que você entrasse na base de dados
                  do PNAD-COVID-19 do IBGE e organizasse esta base para análise,
                  utilizando Banco de Dados em Nuvem e trazendo as seguintes
                  características:
               </p>
               <ol>
                  <li>
                     Utilização de no máximo 20 questionamentos realizados na
                     pesquisa;
                  </li>
                  <li>Utilizar 3 meses para construção da solução;</li>
                  <li>Caracterização dos sintomas clínicos da população;</li>
                  <li>Comportamento da população na época da COVID-19;</li>
                  <li>Características econômicas da Sociedade;</li>
               </ol>
               <p>
                  Seu objetivo será trazer uma breve análise dessas informações,
                  como foi a organização do banco, as perguntas selecionadas
                  para a resposta do problema e quais seriam as principais ações
                  que o hospital deverá tomar em caso de um novo surto de
                  COVID-19.
               </p>
            </section>
         </div>
      </div>
   );
}
