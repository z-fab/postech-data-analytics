import {
   NavigationMenu,
   NavigationMenuItem,
   NavigationMenuList,
} from "./ui/navigation-menu";
import { LinkMenu } from "./LinkMenu";
import { BookMarked, Hospital, PackageSearch, Users } from "lucide-react";
import cover from "../assets/cover.jpg";

export function Header() {
   return (
      <header className="flex flex-col items-center justify-center mt-16">
         <div className="w-2/3 min-w-[500px] max-w-[800px]">
            <img
               src={cover}
               alt="Capa do projeto"
               className="rounded-lg h-40 w-full object-cover shadow-lg mb-8"
            />
            <h1 className="font-bold text-4xl">
               Tech Challenge: <span className="text-green-600">COVID-19</span>
            </h1>
            <p className="mt-4 italic text-zinc-500">
               Tech Challenge é o projeto final de fase da PósTech, ele engloba
               os conhecimentos obtidos em todas as disciplinas vistas até
               aquele momento.
            </p>
            <p className="mt-4 text-zinc-800">
               Você pode acessar o repositório com Notebooks e o código em{" "}
               <a
                  target="_blank"
                  className="text-green-600 underline underline-offset-4 hover:animate-pulse"
                  href="https://github.com/z-fab/postech-data-analytics/tree/master/tech-challenge/f3-covid"
               >
                  Repositório Github
               </a>{" "}
               e me encontrar no linkedin como{" "}
               <a
                  target="_blank"
                  className="text-green-600 underline underline-offset-4 hover:animate-pulse"
                  href="https://www.linkedin.com/in/fazillig/"
               >
                  Fabricio Zillig
               </a>
            </p>

            <nav className="flex items-start mt-12 -ml-4 border-b pb-3 border-zinc-200">
               <NavigationMenu>
                  <NavigationMenuList>
                     <NavigationMenuItem>
                        <LinkMenu to="/">
                           <BookMarked className="mr-2" /> 1. Contexto
                        </LinkMenu>
                     </NavigationMenuItem>
                     <NavigationMenuItem>
                        <LinkMenu to="/processo">
                           <PackageSearch className="mr-2" /> 2. Processo
                        </LinkMenu>
                     </NavigationMenuItem>
                     <NavigationMenuItem>
                        <LinkMenu to="/relatorio">
                           <Hospital className="mr-2" /> 3. Relatório
                        </LinkMenu>
                     </NavigationMenuItem>
                     <NavigationMenuItem>
                        <LinkMenu to="/cluster">
                           <Users className="mr-2" /> 4. Clusterização
                        </LinkMenu>
                     </NavigationMenuItem>
                  </NavigationMenuList>
               </NavigationMenu>
            </nav>
         </div>
      </header>
   );
}
