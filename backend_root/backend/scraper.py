import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import arrow
import jmespath
from scrapfly import ScrapeApiResponse, ScrapeConfig, ScrapflyClient
from typing_extensions import TypedDict

scrapfly = ScrapflyClient(key="YOUR SCRAPFLY KEY", max_concurrency=2)

def extract_cache(react_initial_context):
    """extract microservice cache data from the react server agent"""
    result = {}
    for name, cache in react_initial_context["ReactServerAgent.cache"]["dataCache"].items():
        # first we retrieve cached response and see whether it's a success
        try:
            cache_response = cache["res"]
        except KeyError:  # empty cache
            continue
        if cache_response.get("status") != 200:
            print("skipping non 200 cache")
            continue
        # then extract cached response body and interpret it as a JSON
        cache_data = cache_response.get("body", {}).get("payload")
        if not cache_data:
            cache_data = json.loads(cache_response["text"].split("&&", 1)[-1]).get("payload")
        if not cache_data:
            # skip empty caches
            continue
        # for Redfin we can cleanup cache names for home data endpoints:
        if "/home/details" in name:
            name = name.split("/home/details/")[-1]
        result[name.replace("/", "")] = cache_data
        # ^note: we sanitize name to avoid slashes as they are not allowed in JMESPath
    return result


class PropertyResult(TypedDict):
    """type hint for property result. i.e. Defines what fields are expected in property dataset"""

    photos: List[str]
    videos: List[str]
    price: int
    info: Dict[str, str]
    amenities: List[Dict[str, str]]
    records: Dict[str, str]
    history: Dict[str, str]
    floorplan: Dict[str, str]
    activity: Dict[str, str]


def parse_redfin_proprety_cache(data_cache) -> PropertyResult:
    """parse Redfin's cache data for proprety information"""
    # here we define field name to JMESPath mapping
    parse_map = {
        # from top area of the page: basic info, videos and photos
        "photos": "aboveTheFold.mediaBrowserInfo.photos[*].photoUrls.fullScreenPhotoUrl",
        "videos": "aboveTheFold.mediaBrowserInfo.videos[*].videoUrl",
        "price": "aboveTheFold.addressSectionInfo.priceInfo.amount",
        "info": """aboveTheFold.addressSectionInfo.{
            bed_num: beds,
            bath_numr: baths,
            full_baths_num: numFullBaths,
            sqFt: sqFt,
            year_built: yearBuitlt,
            city: city,
            state: state,
            zip: zip,
            country_code: countryCode,
            fips: fips,
            apn: apn,
            redfin_age: timeOnRedfin,
            cumulative_days_on_market: cumulativeDaysOnMarket,
            property_type: propertyType,
            listing_type: listingType,
            url: url
        }
        """,
        # from bottom area of the page: amenities, records and event history
        "amenities": """belowTheFold.amenitiesInfo.superGroups[].amenityGroups[].amenityEntries[].{
            name: amenityName, values: amenityValues
        }""",
        "records": "belowTheFold.publicRecordsInfo",
        "history": "belowTheFold.propertyHistoryInfo",
        # other: sometimes there are floorplans
        "floorplan": r"listingfloorplans.floorPlans",
        # and there's always internal Redfin performance info: views, saves, etc.
        "activity": "activityInfo",
    }
    results = {}
    for key, path in parse_map.items():
        value = jmespath.search(path, data_cache)
        results[key] = value
    return results


def parse_property(result: ScrapeApiResponse) -> PropertyResult:
    script = result.selector.xpath('//script[contains(.,"ServerState.InitialContext")]/text()').get()
    initial_context = re.findall(r"ServerState.InitialContext = (\{.+\});", script)
    if not initial_context:
        print(f"page {result.context['url']} is not a property listing page")
        return
    return parse_redfin_proprety_cache(extract_cache(json.loads(initial_context[0])))


async def scrape_properties(urls: List[str]) -> List[PropertyResult]:
    to_scrape = [ScrapeConfig(url=url, asp=True, country="US", cache=True) for url in urls]
    properties = []
    async for result in scrapfly.concurrent_scrape(to_scrape):
        properties.append(parse_property(result))
    return properties



async def scrape_feed(url) -> Dict[str, datetime]:
    """Scrape Redfin sitemap for URLs"""
    result = await scrapfly.async_scrape(ScrapeConfig(url=url, country="US", cache=True, asp=True))
    results = {}
    for item in result.selector.xpath("//url"):
        url = item.xpath("loc/text()").get()
        pub_date = item.xpath("lastmod/text()").get()
        results[url] = arrow.get(pub_date).datetime
    return results

async def example_run():
  urls = [
      "https://www.redfin.com/FL/Cape-Coral/402-SW-28th-St-33914/home/61856041",
      "https://www.redfin.com/FL/Cape-Coral/4202-NW-16th-Ter-33993/home/62053611",
      "https://www.redfin.com/FL/Cape-Coral/1415-NW-38th-Pl-33993/home/62079956",
      "https://www.redfin.com/FL/Cape-Coral/1026-NE-34th-Ln-33909/home/67830364",
      "https://www.redfin.com/FL/Cape-Coral/1022-NE-34th-Ln-33909/home/62069246",
      "https://www.redfin.com/FL/Cape-Coral/4132-NE-21st-Ave-33909/home/67818227",
      "https://www.redfin.com/FL/Cape-Coral/2115-NW-8th-Ter-33993/home/62069405",
      "https://www.redfin.com/FL/Cape-Coral/1451-Weeping-Willow-Ct-33909/home/178539244",
      "https://www.redfin.com/FL/Cape-Coral/1449-Weeping-Willow-Ct-33909/home/178539243",
      "https://www.redfin.com/FL/Cape-Coral/5431-SW-6th-Ave-33914/home/61888403",
      "https://www.redfin.com/FL/Cape-Coral/1445-Weeping-Willow-Ct-33909/home/178539241",
  ]
    feed = await scrape_feed("https://www.redfin.com/stingray/api/gis-cms/city-sitemap/CA/San-Francisco?channel=buy")
    asyncio.run(scrape_feed("https://www.redfin.com/newest_listings.xml"))


if __name__ == "__main__":
    asyncio.run(example_run())