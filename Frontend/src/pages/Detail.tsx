import { ArrowLeft, Loader2, TriangleAlert } from 'lucide-react'
import { useNavigate, useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import axios from 'axios'

export default function Detail() {
  const { projectId, errorId } = useParams()
  const navigate = useNavigate()

  const fetchVulnerability = async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/vulnerabilities/get-vulnerability/${projectId}/${errorId}`)
    return response.data
  }

  const { data: vulnerability, status } = useQuery({
    queryKey: ['vulnerability', projectId, errorId],
    queryFn: fetchVulnerability,
  })

  if (status === 'loading') {
    return (
      <div className="h-screen flex justify-center items-center">
        <Loader2 className='my-28 h-16 w-16 text-primary/60 animate-spin' />
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="h-screen flex justify-center items-center">
        <p>An error has occurred!</p>
      </div>
    )
  }

  { console.log(vulnerability?.details.replace("\n$", '')) }

  return (
    <main className="max-w-screen-lg mx-auto p-4">
      <div className="grid items-center mb-8">
        <div className="mb-4 flex items-center">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back</span>
          </button>
        </div>
        <p className="text-xl text-gray-600 font-bold">{vulnerability?.cve || vulnerability?.cwe}</p>
        <h1 className="text-4xl font-black tracking-tight">{vulnerability?.vulnerability}</h1>
      </div>

      <div className="flex items-center gap-2 mb-4">
        <TriangleAlert className="bg-indigo-600 text-white rounded-lg p-2 w-10 h-10" />
        <p className="font-bold text-2xl text-indigo-600">Summary of the Vulnerability</p>
      </div>
      <p className="mb-4">{vulnerability?.details.split("\\n")}</p>


      {vulnerability?.last_test ? (
        vulnerability?.last_test.result ? (

          vulnerability.last_test.result.exploitable ? (
            <>
              <div className="mb-4">
                <p className="font-bold text-2xl text-indigo-600 mb-4">Suggestion</p>
                <p>{vulnerability.last_test.result.suggestion}</p>
              </div>
              <div>
                <p className="font-bold text-2xl text-indigo-600 mb-4">Code overview</p>
                <p className="mb-2">Vulnerabilty found on <b>line {vulnerability.last_test.result.line_number}</b></p>
                <div className="border border-black rounded-lg p-4 bg-gray-50">
                  <pre className="whitespace-pre-wrap font-mono text-sm">
                    {vulnerability.last_test.result.file_context.split("\n").map((line, idx) => {
                      const lineNumber = vulnerability.last_test.result.file_context.split("\n")[idx].split("|")[0].trim(); // Extract the line number
                      return (
                        <div
                          key={lineNumber}
                          className={parseInt(lineNumber) === vulnerability.last_test.result.line_number ? "bg-red-200" : ""}
                        >
                          {line}
                        </div>
                      );
                    })}
                  </pre>
                </div>
              </div>
            </>
          ) : (
            <p>This vulnerability was not exploitable</p>
          )
        ) : (
          <p>Failed to test the vulnerability</p>
        )
      ) : (
        <p>Vulnerability not tested yet</p>
      )}
    </main>
  )
}
