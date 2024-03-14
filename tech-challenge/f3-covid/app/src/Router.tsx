import { Route, Routes } from "react-router-dom";
import { DefaultLayout } from "./layouts/DefaultLayout";
import { Contexto } from "./pages/Contexto";
import { Processo } from "./pages/Processo";
import { Cluster } from "./pages/Cluster";
import { Relatorio } from "./pages/Relatorio";

export function Router() {
   return (
      <Routes>
         <Route path="/" element={<DefaultLayout />}>
            <Route path="/" element={<Contexto />} />
            <Route path="/processo" element={<Processo />} />
            <Route path="/relatorio" element={<Relatorio />} />
            <Route path="/cluster" element={<Cluster />} />
         </Route>
      </Routes>
   );
}
