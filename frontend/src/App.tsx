import { useState, type ChangeEvent } from 'react'
import { Upload, Mail, Users, Send, Loader2 } from 'lucide-react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

interface Recruiter {
  id: number
  name: string
  company: string
  title?: string
  email: string
}

interface GeneratedEmail {
  id: number
  subject: string
  body: string
  status: string
  recruiter_id: number
}

function App() {
  const [recruiters, setRecruiters] = useState<Recruiter[]>([])
  const [emails, setEmails] = useState<GeneratedEmail[]>([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [generating, setGenerating] = useState(false)

  const fetchRecruiters = async () => {
    try {
      const res = await axios.get(${API_BASE}/recruiters/)
      setRecruiters(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchEmails = async () => {
    try {
      const res = await axios.get(${API_BASE}/pipeline/generated-emails)
      setEmails(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const uploadPDF = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await axios.post(${API_BASE}/extraction/pdf, formData)
      alert(Uploaded:  saved,  duplicates)
      await fetchRecruiters()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error uploading PDF')
    }
    setUploading(false)
    e.target.value = ''
  }

  const generateDrafts = async (limit: number = 10) => {
    setGenerating(true)
    try {
      await axios.post(${API_BASE}/pipeline/generate-drafts?limit=)
      alert('Draft generation completed')
      await fetchEmails()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error generating drafts')
    }
    setGenerating(false)
  }

  const createGmailDrafts = async (limit: number = 10) => {
    setLoading(true)
    try {
      await axios.post(${API_BASE}/pipeline/create-gmail-drafts?limit=)
      alert('Gmail drafts created')
      await fetchEmails()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error creating gmail drafts')
    }
    setLoading(false)
  }

  const generateForAll = async () => {
    setGenerating(true)
    try {
      await axios.post(${API_BASE}/pipeline/generate-drafts-range?start=1&end=)
      alert('Generated drafts')
      await fetchEmails()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error generating drafts')
    }
    setGenerating(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Recruiter Agent</h1>
          <p className="text-gray-600">Upload PDF ? Generate Draft Emails ? Create Gmail Drafts</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex flex-wrap gap-4 items-center">
            <label className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 cursor-pointer">
              <Upload size={18} />
              {uploading ? 'Uploading...' : 'Upload PDF'}
              <input type="file" accept=".pdf" onChange={uploadPDF} className="hidden" disabled={uploading} />
            </label>
            <button onClick={fetchRecruiters} className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">
              <Users size={18} />
              Refresh Recruiters ({recruiters.length})
            </button>
            <button onClick={() => generateDrafts(10)} disabled={generating} className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">
              {generating && <Loader2 className="animate-spin" size={18} />}
              <Mail size={18} />
              Generate 10 Drafts
            </button>
            {recruiters.length > 0 && (
              <button onClick={generateForAll} disabled={generating} className="flex items-center gap-2 px-4 py-2 bg-green-800 text-white rounded hover:bg-green-900 disabled:opacity-50">
                {generating && <Loader2 className="animate-spin" size={18} />}
                Generate for All ({recruiters.length})
              </button>
            )}
            <button onClick={() => createGmailDrafts(10)} disabled={loading} className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50">
              {loading && <Loader2 className="animate-spin" size={18} />}
              <Send size={18} />
              Create 10 Gmail Drafts
            </button>
            <button onClick={fetchEmails} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
              Refresh Drafts ({emails.length})
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Recruiters ({recruiters.length})</h2>
            <div className="max-h-96 overflow-y-auto">
              {recruiters.map((r) => (
                <div key={r.id} className="border-b py-3">
                  <div className="font-medium">{r.name}</div>
                  <div className="text-sm text-gray-600">{r.company} - {r.title || ''}</div>
                  <div className="text-sm text-gray-500">{r.email}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Generated Drafts ({emails.length})</h2>
            <div className="max-h-96 overflow-y-auto space-y-3">
              {emails.map((e) => (
                <div key={e.id} className="border rounded p-3">
                  <div className="text-sm font-medium text-blue-900">{e.subject}</div>
                  <div className="text-xs text-gray-500 mt-1">Status: {e.status} | ID: {e.id}</div>
                  <div className="text-xs text-gray-600 mt-2 whitespace-pre-wrap max-h-40 overflow-y-auto">{e.body}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App