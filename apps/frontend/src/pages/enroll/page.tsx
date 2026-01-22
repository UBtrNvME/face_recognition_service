import { reatomComponent } from '@reatom/react'
import { useState, useRef, useEffect } from 'react'
import { enrollFace } from './model'
import { userAtom } from '../../model'
import { wrap } from '@reatom/core'

export const EnrollPage = reatomComponent(() => {
  const user = userAtom()
  const [imageSrc, setImageSrc] = useState<string | null>(null)
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [userId, setUserId] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [cameraActive, setCameraActive] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const streamRef = useRef<MediaStream | null>(null)

  // Auto-fill user ID if available
  useEffect(wrap(() => {
    if (user && !userId) {
      setUserId(user.id.toString())
    }
  }), [user, userId])

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        setCameraActive(true)
      }
    } catch (err) {
      setError('Failed to access camera. Please check permissions.')
      console.error('Camera error:', err)
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
    setCameraActive(false)
  }

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current
      const canvas = canvasRef.current
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.drawImage(video, 0, 0)
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' })
            setImageFile(file)
            setImageSrc(URL.createObjectURL(blob))
            stopCamera()
          }
        }, 'image/jpeg', 0.95)
      }
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImageFile(file)
      setImageSrc(URL.createObjectURL(file))
      setError(null)
      setSuccess(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!imageFile) {
      setError('Please select an image or capture from webcam')
      return
    }
    if (!userId) {
      setError('Please enter a user ID')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await enrollFace(parseInt(userId), imageFile)
      setSuccess(`Successfully enrolled ${result.faces_enrolled} face(s) for user ${result.user_id}`)
      setImageFile(null)
      setImageSrc(null)
      if (e.target instanceof HTMLFormElement) {
        e.target.reset()
      }
    } catch (err: any) {
      const errorMessage = err?.response?.data?.detail || err?.message || 'Enrollment failed'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    return () => {
      stopCamera()
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc)
      }
    }
  }, [imageSrc])

  return (
    <div style={{
      minHeight: '100vh',
      padding: '2rem',
      backgroundColor: '#f9fafb',
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '8px',
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
      }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 700,
          marginBottom: '0.5rem',
          textAlign: 'center',
        }}>
          Face Enrollment
        </h1>
        <p style={{
          color: '#6b7280',
          textAlign: 'center',
          marginBottom: '2rem',
        }}>
          Enroll faces for a user using webcam or file upload
        </p>

        <form onSubmit={wrap(handleSubmit)}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <label htmlFor="userId" style={{ fontWeight: 500 }}>
                User ID
              </label>
              <input
                id="userId"
                type="number"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter user ID"
                required
                style={{
                  padding: '0.75rem',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  fontSize: '1rem',
                }}
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  onClick={cameraActive ? stopCamera : startCamera}
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: cameraActive ? '#dc2626' : '#2563eb',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '1rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                  }}
                >
                  {cameraActive ? 'Stop Camera' : 'Start Webcam'}
                </button>
                {cameraActive && (
                  <button
                    type="button"
                    onClick={capturePhoto}
                    style={{
                      padding: '0.75rem 1.5rem',
                      backgroundColor: '#16a34a',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      fontSize: '1rem',
                      fontWeight: 500,
                      cursor: 'pointer',
                    }}
                  >
                    Capture Photo
                  </button>
                )}
                <label
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#6b7280',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '1rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                    display: 'inline-block',
                  }}
                >
                  Upload File
                  <input
                    type="file"
                    accept="image/*"
                    onChange={wrap(handleFileChange)}
                    style={{ display: 'none' }}
                  />
                </label>
              </div>

              {cameraActive && (
                <div style={{ position: 'relative', width: '100%', maxWidth: '640px', margin: '0 auto' }}>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    style={{
                      width: '100%',
                      borderRadius: '8px',
                      border: '2px solid #2563eb',
                    }}
                  />
                  <canvas ref={canvasRef} style={{ display: 'none' }} />
                </div>
              )}

              {imageSrc && !cameraActive && (
                <div style={{ textAlign: 'center' }}>
                  <img
                    src={imageSrc}
                    alt="Preview"
                    style={{
                      maxWidth: '100%',
                      maxHeight: '400px',
                      borderRadius: '8px',
                      border: '2px solid #16a34a',
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => {
                      setImageSrc(null)
                      setImageFile(null)
                    }}
                    style={{
                      marginTop: '0.5rem',
                      padding: '0.5rem 1rem',
                      backgroundColor: '#dc2626',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                    }}
                  >
                    Remove Image
                  </button>
                </div>
              )}
            </div>

            {error && (
              <div style={{
                color: '#dc2626',
                fontSize: '0.875rem',
                padding: '0.75rem',
                backgroundColor: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: '4px',
              }}>
                {error}
              </div>
            )}

            {success && (
              <div style={{
                color: '#16a34a',
                fontSize: '0.875rem',
                padding: '0.75rem',
                backgroundColor: '#f0fdf4',
                border: '1px solid #bbf7d0',
                borderRadius: '4px',
              }}>
                {success}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !imageFile}
              style={{
                padding: '0.75rem 1.5rem',
                backgroundColor: loading || !imageFile ? '#9ca3af' : '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '1rem',
                fontWeight: 500,
                cursor: loading || !imageFile ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.2s',
              }}
            >
              {loading ? 'Enrolling...' : 'Enroll Face'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
})

