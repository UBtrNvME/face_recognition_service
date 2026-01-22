import { action, withAsync, wrap } from '@reatom/core'
import fetches from '@siberiacancode/fetches'
import type { FaceUploadResponse } from '../../model'
import { getAuthHeaders } from '../../utils/api'

export const matchFace = action(
  async (file: File, threshold: number = 0.6, limit: number = 10) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await wrap(
      fetches.post<FaceUploadResponse>(
        `/api/v1/face/match?threshold=${threshold}&limit=${limit}`,
        formData,
        {
          headers: getAuthHeaders(),
        }
      )
    )

    return response.data
  }
).extend(withAsync())

