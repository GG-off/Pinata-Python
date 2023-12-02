from src.pinata import Pinata
import pytest

class TestPinata():

    @pytest.fixture
    def pinata_inputs(self):
        api_key = ""     
        secret_key = ""
        access_token = ""

        return {'api_key': api_key, 'secret_key': secret_key, 'access_token': access_token}

    def test_no_credentials(self):
        pinata = Pinata("", "", "")
        pins = pinata.get_pins()
        assert pins["status"], "error"

    def test_missing_access_token(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        pins = pinata.get_pins()
        assert pins["status"], "error"


    def test_get_pins_success(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        pins = pinata.get_pins()
        assert (pins["status"] == "success")

    def test_pin_nonexistent_local_file(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        pins = pinata.pin_file('non_existent_file.txt')
        assert (pins["status"] == "error")
        assert (pins["message"] == 'File does not exist')

    def test_pin_file_success(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        open("test.txt", 'w').write("Test file")
        pin = pinata.pin_file('/tmp/test.txt')
        assert(pin['status'] == "success")

    def test_unip_non_existent_file(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        unpin = pinata.unpin_file("xxxxxxxxxxxxxxxxxxxxxxx")
        assert(unpin['status'] == 'error')
        assert(unpin['message'] == 'The current user has not pinned the cid: xxxxxxxxxxxxxxxxxxxxxxx')

    def test_unpin_file_success(self, pinata_inputs):
        api_key = pinata_inputs["api_key"]
        secret_key = pinata_inputs["secret_key"]
        access_token = pinata_inputs["access_token"]
        pinata = Pinata(api_key, secret_key, access_token)
        open("test.txt", 'w').write("Test file")
        pin = pinata.pin_file('/tmp/test.txt')
        unpin = pinata.unpin_file(pin['data']['IpfsHash'])
        assert(unpin['status'] == 'success')
