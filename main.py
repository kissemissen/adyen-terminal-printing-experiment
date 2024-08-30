import pprint
import random
import constants
import requests
import json
import pyqrcode
import time
import uuid
import base64
from PIL import Image
from io import BytesIO


def main():
    number_of_qr_codes = 5
    # start timer
    start_time = time.time()
    # print_qrcode_native(number_of_qr_codes)
    print_qrcode_image(number_of_qr_codes)
    print(f'Printing speed for {number_of_qr_codes}: {time.time() - start_time}')


def print_qrcode_native(number_of_qr_codes):
    for _ in range(number_of_qr_codes):
        tapi_request(get_dict_qr())


def print_qrcode_image(number_of_qr_codes):
    for i in range(0, number_of_qr_codes):
        qr_content = pyqrcode.create(f'{uuid.uuid4()}')
        # print(qr_content.terminal())
        # with open('qr_code.png', 'wb') as fstream:
        #     qr_content.png(fstream, scale=5)
        qr_content.png(f'qr_code_{i}.png', scale=5)

    # define total image dimension based on number of qr codes + 100 px
    width = 380
    height = 250 * number_of_qr_codes
    receipt_image = Image.new("RGB", (width, height), (255, 255, 255))

    opened_qr_codes = []
    for qr_file_number in range(0, number_of_qr_codes):
        opened_qr_codes.append(Image.open(f'qr_code_{qr_file_number}.png'))

    print(opened_qr_codes)

    x_start_position = (width - opened_qr_codes[0].width) / 2
    # px cannot be float variable, cast to int
    x_start_position = int(x_start_position)

    # start with pasting image at (x_start_position, y_position)
    y_position = 0
    for qr_code in opened_qr_codes:
        receipt_image.paste(qr_code, (x_start_position, y_position))
        y_position = y_position + 250

    # Save image to file
    # receipt_image.save("receipt_image.png")

    # Saving image not necessary, write directly to memory buffer
    buffered = BytesIO()
    receipt_image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # print(f'Decoded image: {buffered.getvalue()}')
    print(f'Encoded image: {encoded_image}')

    # with open("receipt_image.png", "rb") as f:
    #     encoded_image = base64.b64encode(f.read())
    #     print(encoded_image)

    image_xml_code = f'<?xml version="1.0" encoding="UTF-8"?><img src="data:image/png;base64, {encoded_image}"/>'
    print(image_xml_code)
    encoded_image_xml_code = base64.b64encode(image_xml_code.encode()).decode('utf-8')
    print(encoded_image_xml_code)

    # Call Adyen
    tapi_request(get_dict_image(encoded_image_xml_code))


def tapi_request(request_dict: dict):
    """
    Call Adyen cloud endpoint with request body. Takes a request dict and converts it to json body before call.
    :param request_dict:
    :return:
    """
    request_url = constants.ADYEN_TERMINAL_ENDPOINT_CLOUD_URL
    request_headers = {
        'x-API-key': constants.ADYEN_X_API_KEY,
        'Content-Type': 'application/json'
    }
    request_body = json.dumps(request_dict)
    pprint.pprint(request_body)
    request = requests.post(
        url=request_url,
        headers=request_headers,
        data=request_body
    )
    # print response
    pprint.pprint(request.text)


def get_dict_qr() -> dict:
    return {
        "SaleToPOIRequest": {
            "MessageHeader": {
                "ProtocolVersion": "3.0",
                "MessageClass": "Device",
                "MessageCategory": "Print",
                "MessageType": "Request",
                "ServiceID": f"SID{random.randint(1000, 9999)}",
                "SaleID": "POSSystemID12345",
                "POIID": "S1F2-000158204800498"
            },
            "PrintRequest": {
                "PrintOutput": {
                    "DocumentQualifier": "CustomerReceipt",
                    "ResponseMode": "PrintEnd",
                    "OutputContent": {
                        "OutputFormat": "BarCode",
                        "OutputBarcode": {
                            "BarcodeType": "QRCode",
                            "BarcodeValue": f"{uuid.uuid4()}"
                        }
                    }
                }
            }
        }
    }


def get_dict_image(encoded_xml: str) -> dict:
    return {
        "SaleToPOIRequest": {
            "MessageHeader": {
                "ProtocolVersion": "3.0",
                "MessageClass": "Device",
                "MessageCategory": "Print",
                "MessageType": "Request",
                "ServiceID": f"SID{random.randint(1000, 9999)}",
                "SaleID": "POSSystemID12345",
                "POIID": "S1F2-000158204800498"
            },
            "PrintRequest": {
                "PrintOutput": {
                    "DocumentQualifier": "Document",
                    "ResponseMode": "PrintEnd",
                    "OutputContent": {
                        "OutputFormat": "XHTML",
                        "OutputXHTML": encoded_xml
                    }
                }
            }
        }
    }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
