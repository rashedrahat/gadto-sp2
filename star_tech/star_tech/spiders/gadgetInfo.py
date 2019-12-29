# -*- coding: utf-8 -*-
import scrapy
from ..items import StarTechItem
import re


class StarTechSpider(scrapy.Spider):
    name = 'starTech'
    # allowed_domains = ['startech.com.bd/desktops/brand-pc']
    start_urls = ['https://startech.com.bd/desktops/brand-pc', 'https://www.startech.com.bd/laptop-notebook/laptop',
                  'https://www.startech.com.bd/monitor', 'https://www.startech.com.bd/accessories/keyboards',
                  'https://www.startech.com.bd/networking/router', 'https://www.startech.com.bd/gadget/smart-watch',
                  'https://www.startech.com.bd/camera/camera-dslr']

    def parse(self, response):
        gadgets = response.css('.product-thumb')

        for gadget in gadgets:
            link = gadget.css('.product-name a::attr(href)').get()

            yield response.follow(link, self.parse_details)

        next_page = response.xpath(
            ".//ul/ul/li/a[text()='NEXT']/@href").extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        items = StarTechItem()

        gad_name = response.css(
            '.product-short-info .product-name::text').extract_first()
        items['gadget_name'] = gad_name

        gad_name_li = gad_name.split()

        items['gadget_model'] = ""
        for i in gad_name_li:
            if bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])|(?=.*[a-zA-Z]$)(?=.*[0-9])', i)):
                items['gadget_model'] = i
                break

        if items['gadget_model'] == "":
            items['gadget_model'] = "NA"

        gad_cat = response.xpath(
            ".//ul[@class='breadcrumb']/li[2]/a/span/text()").extract_first()

        if gad_cat in ["Desktop PC", "Laptop & Netbook", "Monitor", "Accessories", "Gadget", "Networking", "Camera"]:
            if gad_cat == "Desktop PC":
                items['gadget_category'] = "Desktop"
            elif gad_cat == "Laptop & Netbook":
                items['gadget_category'] = "Laptop"
            elif gad_cat == "Monitor":
                items['gadget_category'] = "Monitor"
            elif gad_cat == "Accessories":
                items['gadget_category'] = "Keyboard"
            elif gad_cat == "Gadget":
                items['gadget_category'] = "Smart Watch"
            elif gad_cat == "Networking":
                items['gadget_category'] = "Router"
            else:
                items['gadget_category'] = "Camera"

        # if gad_cat in ["Accessories", "Gadget", "Networking"]:
        #     items['gadget_category'] = response.xpath(".//ul[@class='breadcrumb']/li[3]/a/span/text()").extract_first()
        # else:
        #     items['gadget_category'] = response.xpath(".//ul[@class='breadcrumb']/li[2]/a/span/text()").extract_first()

        items['gadget_brand'] = response.css(
            '.product-info-group+ .product-info-group .product-price::text').extract()
        items['gadget_price'] = response.css(
            '.product-info-group:nth-child(1) .product-price::text').extract()
        # items['gadget_specification'] = response.css('#description p::text').extract()
        items['gadget_specification'] = response.css(
            '.short-description ul li::text').extract()
        items['gadget_img_url'] = response.css('.main-img::attr(src)').get()
        items['e_commerce_website'] = "Star Tech"
        items['gadget_url'] = response.url

        yield items

        self.parse
