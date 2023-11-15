import face_recognition


def generate_face_encoding_from_image(upload_file):
    image = face_recognition.load_image_file(upload_file.file)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        return None
    return face_encodings[0]
