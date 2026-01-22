import { action, withAsync, wrap } from '@reatom/core'
import fetches from '@siberiacancode/fetches'
import type { FaceEnrollResponse } from '../../model'
import { getAuthHeaders } from '../../utils/api'

export const enrollFace = action(
  async (userId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await wrap(
      fetches.post<FaceEnrollResponse>(
        `/api/v1/face/enroll?user_id=${userId}`,
        formData,
        {
          headers: getAuthHeaders(),
        }
      )
    )

    return response.data
  }
).extend(withAsync())

