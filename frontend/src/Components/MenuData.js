import React from 'react'
import * as AiIcons from "react-icons/ai"
import * as FaIcons from "react-icons/fa"

export const MenuData = 
   [
      {
         title: 'Stocks',
         path: '/Stocks',
         icon: <AiIcons.AiOutlineStock/>,
      },
      {
         title: 'News',
         path: '/News',
         icon: <AiIcons.AiOutlineWhatsApp />,
      },
      {
         title: 'Portfolio',
         path: '/Portfolio',
         icon: <AiIcons.AiOutlineProfile />,
      },
      {
         title: 'ML/AI',
         path: '/ML',
         icon: <AiIcons.AiOutlineRobot/>,
      },
      {
         title: 'Support',
         path: '/Contact',
         icon: <FaIcons.FaHandsHelping />,
      },
   ]