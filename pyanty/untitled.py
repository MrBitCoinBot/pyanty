import asyncio
import random
import pyanty as dolphin
from pyanty import DolphinAPI, STABLE_CHROME_VERSION

api = DolphinAPI(api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNWQxNGQ0ZDJmYzE0OTVkZTg0NWMyODcxNTM0MTg0YjA4ZTM2MzIyYjFlNzg5YzY5MGZmMGQzYmNmMzk2NmM1OGYxZmZmZmFlNDljNGYzZDAiLCJpYXQiOjE3MjM5OTQ0MzIuMTY3NjE0LCJuYmYiOjE3MjM5OTQ0MzIuMTY3NjE2LCJleHAiOjE3NTU1MzA0MzIuMTU3NjY3LCJzdWIiOiIzNjYxNzkzIiwic2NvcGVzIjpbXX0.b0fKMFUAOi8zOqeF9w5y43NBQx_vu64L93w3fHTN5UmO0gIhm7rUQy5kNkx65ppZX3hF9mxsOt7esBJTa7Vpxqai2wViGHEkSYVtDuRUQVBqbZ6GzkmGeBqZTmsUI-2aEOKjKKAd734fMU27NcMDbja8id2ESnNzWwJUU4plxi2P_psK1X9fOygBjRB_Pkn0GZEipTAr3dG9JeRedMcYt_F9AhoS2oax9ZTA5W77m2dcf9QRBUSmDb2PRjySR8HzNhDPytdkA1FHBeID3amOcVweLDj2H6usk1jAQnrUW9jIUNnGJdHNRTnu0w9LLarYj_htFQVTjYPREL-cCCywFbXR8GI0cgJj1CWvNiMmSKw_xtqr9xV3UpB-9SUfvNgZPBRTvYvf8RHC_aR9qTpHMezRxrNHvWsczspqa1eJkmEnUSsLoZqZj9IpXZDP3PqPUi5mF-rz-ui4JMr0gLGLF0gOQT6QVsM0f5B4p58vnYcYFBm8GGcmC5RtBEiTeILwJDA5F-pQ8jBIYAL1Es_xo89yvKsOTecLBj3I-hSsL93YA44G3LRXXizS8fcV1ZhJtVu2-rZ13cuAAOih18ouJuMAsAmvVJvAHWRhB1n-JGWPhldrV3iNVGcLmWCOpbuFcMLvvm6ee-5Us7Z9yI50up-v26QY4Zo7LGYCkqBufE4')

response = api.get_profiles()
if response['data']:
    profile_id = response['data'][-1]['id']
    if profile_id:
        api.delete_profiles([profile_id])

fingerprint = []
while not fingerprint:
  fingerprint = api.generate_fingerprint(platform='windows', browser_version=f'{random.randint(114, STABLE_CHROME_VERSION)}')

data = api.fingerprint_to_profile(name='my superprofile', fingerprint=fingerprint)

profile_id = api.create_profile(data)['browserProfileId']


headless = True
response = dolphin.run_profile(profile_id, headless)
port = response['automation']['port']
ws_endpoint = response['automation']['wsEndpoint']

async def main():
    browser = await dolphin.get_browser(ws_endpoint, port, core='playwright')
    pages = browser.pages()
    page = pages[0]
    await page.goto('http://google.com/')
    await asyncio.sleep(5)
    await browser.disconnect()

asyncio.run(main())
dolphin.close_profile(profile_id)