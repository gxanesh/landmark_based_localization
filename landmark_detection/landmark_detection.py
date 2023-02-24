

"""
For more information, the documentation at
https://cloud.google.com/vision/docs.
Example Usage:
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
"""
import warnings as warn
warn.filterwarnings("ignore")

import argparse

def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_landmark_detection]
# [END vision_landmark_detection]


# [START vision_landmark_detection_gcs]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
# [END vision_landmark_detection_gcs]


# [START vision_logo_detection]
def detect_logos(path):
    """Detects logos in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_logo_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_logo_detection]
# [END vision_logo_detection]

def run_local(args):
    if args.command == 'faces':
        detect_faces(args.path)
    elif args.command == 'labels':
        detect_labels(args.path)
    elif args.command == 'landmarks':
        detect_landmarks(args.path)

def run_uri(args):
    if args.command == 'text-uri':
        detect_text_uri(args.uri)
    elif args.command == 'faces-uri':
        detect_faces_uri(args.uri)
    elif args.command == 'labels-uri':
        detect_labels_uri(args.uri)
    elif args.command == 'landmarks-uri':
        detect_landmarks_uri(args.uri)

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    detect_landmarks_parser = subparsers.add_parser('landmarks', help=detect_landmarks.__doc__)
    detect_landmarks_parser.add_argument('path')

    landmark_file_parser = subparsers.add_parser('landmarks-uri', help=detect_landmarks_uri.__doc__)
    landmark_file_parser.add_argument('uri')

    args = parser.parse_args()
    if 'uri' in args.command:
        run_uri(args)
    else:
        run_local(args)
