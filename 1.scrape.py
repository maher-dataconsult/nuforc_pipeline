import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time

async def scrape_ufo_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set user agent to avoid detection
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        
        print('Navigating to the page...')
        await page.goto('https://nuforc.org/subndx/?id=all', wait_until='networkidle')
        
        # Wait for the table to load
        await page.wait_for_selector('table.wpDataTable', timeout=10000)
        
        # Find and set the maximum rows per page (common for wpDataTables)
        select_selector = 'select[name="wpDataTables_filter[1]_length"], .dataTables_length select'
        try:
            rows_per_page_select = await page.query_selector(select_selector)
            if rows_per_page_select:
                max_option = await page.evaluate('''(select) => {
                    const options = Array.from(select.querySelectorAll('option'));
                    return options.reduce((max, opt) => {
                        const val = parseInt(opt.value);
                        return val > max.value ? { value: val, text: opt.textContent } : max;
                    }, { value: 10, text: '' }).value;
                }''', rows_per_page_select)
                
                await page.select_option(select_selector, str(max_option))
                await asyncio.sleep(1)  # Wait for table to reload
                print(f'Set rows per page to {max_option}')
            else:
                print('No rows per page select found, proceeding with default')
        except Exception as err:
            print(f'Could not set rows per page: {err}')
        
        all_data = []
        current_page = 1
        has_next = True
        
        while has_next:
            print(f'Scraping page {current_page}...')
            
            # Wait for table rows
            await page.wait_for_selector('table.wpDataTable tbody tr', timeout=5000)
            
            # Extract rows
            page_data = await page.evaluate('''() => {
                const rows = Array.from(document.querySelectorAll('table.wpDataTable tbody tr'));
                return rows.map(row => {
                    const cells = Array.from(row.querySelectorAll('td'));
                    if (cells.length >= 9) {  // Adjust based on columns
                        return {
                            status: cells[0]?.textContent?.trim() || '',
                            link: cells[0]?.querySelector('a')?.getAttribute('href') || '',
                            occurred: cells[1]?.textContent?.trim() || '',
                            city: cells[2]?.textContent?.trim() || '',
                            state: cells[3]?.textContent?.trim() || '',
                            country: cells[4]?.textContent?.trim() || '',
                            shape: cells[5]?.textContent?.trim() || '',
                            summary: cells[6]?.textContent?.trim() || '',
                            reported: cells[7]?.textContent?.trim() || '',
                            media: cells[8]?.textContent?.trim() || '',
                            explanation: cells[9]?.textContent?.trim() || ''
                        };
                    }
                    return null;
                }).filter(row => row !== null);
            }''')
            
            all_data.extend(page_data)
            print(f'Extracted {len(page_data)} rows from page {current_page}. Total so far: {len(all_data)}')
            
            # Check for next page
            has_next = await page.evaluate('''() => {
                const nextButton = document.querySelector('.paginate_button.next:not(.disabled)');
                return nextButton !== null;
            }''')
            
            if has_next:
                await page.click('.paginate_button.next')
                await asyncio.sleep(1)  # Wait for next page to load
                current_page += 1
                
                # Rate limiting: wait longer if needed
                if current_page % 10 == 0:
                    print('Taking a break to avoid rate limiting...')
                    await asyncio.sleep(3)
        
        await browser.close()
        
        print(f'Scraping complete. Total records: {len(all_data)}')
        
        # Export to CSV
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_csv('ufo_reports.csv', index=False)
            print('Data exported to ufo_reports.csv')
        else:
            print('No data to export')
        
        return len(all_data)

if __name__ == '__main__':
    asyncio.run(scrape_ufo_data())