import { NavLink } from "react-router-dom";
import { navigationMenuTriggerStyle } from "./ui/navigation-menu";

export function LinkMenu({
   to = "/",
   children,
}: {
   to?: string;
   children: React.ReactNode;
}) {
   return (
      <NavLink
         to={to}
         className={({ isActive }) => {
            if (isActive) {
               return "text-green-600 " + navigationMenuTriggerStyle();
            }
            return navigationMenuTriggerStyle();
         }}
      >
         {children}
      </NavLink>
   );
}
