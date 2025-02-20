from playwright.sync_api import sync_playwright

#play = sync_playwright().start()
#play.stop()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel='chrome', headless=False)
    page = browser.new_page(viewport={'width':1980, 'height':2000})

    page.goto('https://search.naver.com/search.naver?sm=tab_sug.asiw&where=nexearch&ssc=tab.nx.all&query=논현동 날씨')

    weather_info = page.locator('div._tab_flicking')
    weather_info.screenshot(path='info.png')