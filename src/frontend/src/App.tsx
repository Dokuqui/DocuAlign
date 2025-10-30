import './App.css'
import { FileUpload } from './components/FileUpload';

function App() {
  return (
    <>
      <h1>DocuAlign 📄</h1>
      <div className="card">
        <FileUpload />
      </div>
    </>
  )
}

export default App