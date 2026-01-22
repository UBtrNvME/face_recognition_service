import './debug' // import before the app!
import React from 'react'
import ReactDOM from 'react-dom/client'
import { clearStack, context } from "@reatom/core"
import { reatomContext } from '@reatom/react'
import { App } from './app/App'
import './index.css'

clearStack()
const root = ReactDOM.createRoot(document.getElementById('root')!)
root.render(
  <reatomContext.Provider value={context.start()}>
      <App />
  </reatomContext.Provider>
)
