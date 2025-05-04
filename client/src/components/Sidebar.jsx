import { ChevronFirst, ChevronLast, MoreVertical } from "lucide-react"
import logo from "../assets/react.svg"
import profile from "../assets/react.svg"
import { createContext, useContext, useState } from "react"
import { NavLink } from 'react-router-dom';

const SidebarContext = createContext();

export default function Sidebar({ children }) {
    const [expanded, setExpanded] = useState(true)
    return (
        <>
            <aside className="h-screen">
                <nav className="h-full flex flex-col bg-white border-r shadow-sm">
                    <div className="p-4 pb-2 flex justify-between items-center">
                        <img src={logo} className={`overflow-hidden transition-all ${expanded ? "w-20" : "w-0"}`} />
                        <button onClick={() => setExpanded((curr) => !curr)} className="p-1.5 rounded-lg bg-gray-50 hover:bg-gray-100">
                            {expanded ? <ChevronFirst /> : <ChevronLast />}
                        </button>
                    </div>

                    <SidebarContext.Provider value={{ expanded }}>
                        <ul className="flex-1 px-3">{children}</ul>
                    </SidebarContext.Provider>

                    <div className="border-t flex p-3">
                        <img src={profile} className="w-10 h-10 rounded-md" />
                        <div className={`flex justify-between items-center overflow-hidden transition-all ${expanded ? "w-52 ml-3" : "w-0"} `}>
                            <div className="leading-4">
                                <h4 className="font-semibold">Pracalit</h4>
                                <span className="text-xs text-gray-600">Transliteration System</span>
                            </div>
                      
                        </div>
                    </div>
                </nav>
            </aside>
        </>
    )
}

export function SidebarItem({ icon, text, to, alert, active }) {
  const { expanded } = useContext(SidebarContext);

  return (
      <NavLink
          to={to}
          className={({ isActive }) => {
              const highlight = active ?? isActive;
              return `relative flex items-center ${
                  expanded ? "py-1" : "py-0.5"
              } px-3 my-1 rounded-md transition-colors group ${
                  highlight
                      ? "bg-gradient-to-tr from-blue-200 to-blue-100 text-blue-800 font-bold"
                      : "hover:bg-blue-50 text-gray-600 font-medium"
              }`;
          }}
      >
          {icon}
          <span className={`overflow-hidden transition-all ${expanded ? "w-52 ml-3" : "w-0"}`}>
              {text}
          </span>

          {alert && (
              <div
                  className={`absolute right-2 w-2 h-2 rounded bg-blue-400 ${expanded ? "" : "top-2"}`}
              />
          )}

          {!expanded && (
              <div className="absolute left-full rounded-md px-2 py-1 ml-6 bg-blue-100 text-blue-800 text-sm invisible opacity-20 -translate-x-3 transition-all group-hover:visible group-hover:opacity-100 group-hover:translate-x-0">
                  {text}
              </div>
          )}
      </NavLink>
  );
}
