import React from "react";
import "../css/Sidebar.css";
import * as RxIcons from "react-icons/rx";
import { MenuData } from "./MenuData";

function SidebarMenu(props) {
   if (props.status === true ) {
      return (
         <div className="mobile-menu">
            <h1> MENU
               <RxIcons.RxExit onClick={props.onClick} className="exit"/> </h1>
            { MenuData.map( (item, index) => {
               return (
                  <li key={index} className="mobile-menu-text">
                     <a href={item.path}>
                        {item.icon}
                        <span> {item.title} </span>
                     </a>
                  </li>
               )})
            }
         </div>
      )
   }
}


export default SidebarMenu