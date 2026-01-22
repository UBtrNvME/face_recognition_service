import { reatomComponent } from '@reatom/react'
import { useState, useRef, useEffect } from 'react'
import { matchFace } from './model'
import type { FaceMatch } from '../../model'
import { wrap } from '@reatom/core'
export const MatchPage = reatomComponent(() => {
    const [imageSrc, setImageSrc] = useState<string | null>(null)
    const [imageFile, setImageFile] = useState<File | null>(null)
    const [threshold, setThreshold] = useState<string>('0.6')
    const [limit, setLimit] = useState<string>('10')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [results, setResults] = useState<{ detected_faces: number; matches: FaceMatch[] } | null>(null)
    const [cameraActive, setCameraActive] = useState(false)
    const videoRef = useRef<HTMLVideoElement>(null)
    const canvasRef = useRef<HTMLCanvasElement>(null)
    const streamRef = useRef<MediaStream | null>(null)

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
            setResults(null)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!imageFile) {
            setError('Please select an image or capture from webcam')
            return
        }

        setLoading(true)
        setError(null)
        setResults(null)

        try {
            const result = await matchFace(
                imageFile,
                parseFloat(threshold),
                parseInt(limit)
            )
            setResults(result)
        } catch (err: any) {
            const errorMessage = err?.response?.data?.detail || err?.message || 'Matching failed'
            setError(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    useEffect(wrap(() => {
        return () => {
            stopCamera()
            if (imageSrc) {
                URL.revokeObjectURL(imageSrc)
            }
        }
    }), [imageSrc])

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
                    Face Matching
                </h1>
                <p style={{
                    color: '#6b7280',
                    textAlign: 'center',
                    marginBottom: '2rem',
                }}>
                    Match faces against enrolled database using webcam or file upload
                </p>

                <form onSubmit={wrap(handleSubmit)}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <label htmlFor="threshold" style={{ fontWeight: 500 }}>
                                    Threshold (0.0 - 1.0)
                                </label>
                                <input
                                    id="threshold"
                                    type="number"
                                    min="0"
                                    max="1"
                                    step="0.1"
                                    value={threshold}
                                    onChange={(e) => setThreshold(e.target.value)}
                                    style={{
                                        padding: '0.75rem',
                                        border: '1px solid #ccc',
                                        borderRadius: '4px',
                                        fontSize: '1rem',
                                    }}
                                />
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <label htmlFor="limit" style={{ fontWeight: 500 }}>
                                    Max Matches (1 - 100)
                                </label>
                                <input
                                    id="limit"
                                    type="number"
                                    min="1"
                                    max="100"
                                    value={limit}
                                    onChange={(e) => setLimit(e.target.value)}
                                    style={{
                                        padding: '0.75rem',
                                        border: '1px solid #ccc',
                                        borderRadius: '4px',
                                        fontSize: '1rem',
                                    }}
                                />
                            </div>
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
                                            setResults(null)
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

                        {results && (
                            <div style={{
                                padding: '1rem',
                                backgroundColor: '#f0f9ff',
                                border: '1px solid #bae6fd',
                                borderRadius: '4px',
                            }}>
                                <h3 style={{ marginTop: 0, marginBottom: '0.5rem' }}>
                                    Results
                                </h3>
                                <p style={{ margin: '0.5rem 0' }}>
                                    <strong>Detected Faces:</strong> {results.detected_faces}
                                </p>
                                {results.matches.length > 0 ? (
                                    <div>
                                        <p style={{ margin: '0.5rem 0', fontWeight: 500 }}>
                                            Matches:
                                        </p>
                                        <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
                                            {results.matches.map((match, index) => (
                                                <li key={index} style={{ margin: '0.25rem 0' }}>
                                                    User ID: {match.user_id}, Distance: {match.distance.toFixed(4)}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ) : (
                                    <p style={{ margin: '0.5rem 0', color: '#6b7280' }}>
                                        No matches found
                                    </p>
                                )}
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
                            {loading ? 'Matching...' : 'Match Face'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
})

