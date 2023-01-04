import re
import requests
import typing as t
from bs4 import BeautifulSoup

from . import PKG_DATA, dc_json as json
from .card import Card, UnitCard, Attack, EffectAttack


def main():
    cards = list(get_wiki_cards())
    write_wiki_cards(cards)


def get_wiki_cards():
    page = get_wiki_page()
    soup = get_soup(page.text)
    boxes = get_info_boxes(soup)
    return WikiCardFactory.from_info_boxes(boxes)


def write_wiki_cards(cards):
    card_list = PKG_DATA / "card-list.json"
    card_list.parent.mkdir(parents=True, exist_ok=True)
    with card_list.open("w") as fp:
        json.dump(cards, fp, indent=4)


def get_wiki_page():
    return requests.get(
        "https://digimon.fandom.com/wiki/Digimon_Digital_Card_Battle/Cards"
    )


def get_soup(doc: str):
    return BeautifulSoup(doc, features="lxml")


def get_info_boxes(soup):
    return (
        soup.html.body.find("div", attrs={"class": "main-container"})
        .find("div", attrs={"class": "resizable-container"})
        .find("div", attrs={"class": "page has-right-rail"})
        .main.find("div", attrs={"class": "page-content"})
        .find("div", attrs={"class": "mw-content-ltr"})
        .find("div", attrs={"class": "mw-parser-output"})
        .find_all(class_="portable-infobox")
    )


class WikiCardFactory:
    ATTACK_BUTTONS = {"c": UnitCard.C_STR, "t": UnitCard.T_STR, "x": UnitCard.X_STR}
    RE_IMG_LINKS: t.Dict[str, re.Pattern] = {
        text: re.compile(f'<img alt="B {button}.gif".*?>')
        for button, text in ATTACK_BUTTONS.items()
    }

    @classmethod
    def from_info_boxes(cls, boxes):
        for b in boxes:
            yield cls.from_info_box(b)

    @classmethod
    def from_info_box(cls, box):
        text = clean_str(box)
        tags = cls._get_info_tags(text)
        return cls.from_info_tags(tags)

    @staticmethod
    def _get_info_tags(text: str):
        return list(find_all_of_tag(text, "td")) + list(find_all_of_tag(text, "div"))

    @classmethod
    def _replace_image_links(cls, text: str):
        for attack_string, pattern in cls.RE_IMG_LINKS.items():
            text = pattern.sub(attack_string, text)
        return text

    @classmethod
    def from_info_tags(cls, tags):
        tags = [cls._replace_image_links(tag) for tag in tags]

        if cls._is_option_card(tags):
            card = cls._card_from_info_tags(tags)
        else:
            card = cls._unitcard_from_info_tags(tags)

        return card

    @staticmethod
    def _is_option_card(tags):
        return len(tags) < 14

    @staticmethod
    def _card_from_info_tags(tags):
        _id, name = tags[0].rsplit("</b>")[0].rsplit("<b>")[-1].split(": ")
        support = tags[1].rsplit('"effect">')[-1]
        return Card(id=int(_id), name=name, support=support)

    @classmethod
    def _unitcard_from_info_tags(cls, tags):
        _id = tags[0].rsplit("<b>")[-1].split(":")[0]

        (
            level,
            specialty,
            _,
            name,
            c_attack,
            t_attack,
            x_attack,
            hp,
            dp,
            pp,
        ) = cls._parse_basic_unitcard_tags(tags[1:-3])

        support = tags[3].rsplit('"support">')[-1]
        c_damage, t_damage, x_damage, x_effect = cls._parse_attack_tags(tags[-3:])

        return UnitCard(
            id=int(_id),
            name=name,
            support=support,
            level=level,
            specialty=specialty,
            hp=int(hp),
            dp=int(dp),
            pp=int(pp),
            c_attack=Attack(name=c_attack, damage=c_damage),
            t_attack=Attack(name=t_attack, damage=t_damage),
            x_attack=EffectAttack(name=x_attack, damage=x_damage, effect=x_effect),
        )

    @staticmethod
    def _parse_basic_unitcard_tags(tags):
        return [tag.rsplit("<br/>")[0].rsplit(">")[-1] for tag in tags]

    @staticmethod
    def _parse_attack_tags(tags):
        c_damage, t_damage, x_info = [tag.rsplit("<br/>")[-1] for tag in tags[:3]]
        x_damage, x_effect = x_info.split(", ", maxsplit=1)

        c_damage, t_damage, x_damage = [
            int(damage[1:-1]) for damage in (c_damage, t_damage, x_damage)
        ]
        return c_damage, t_damage, x_damage, x_effect


def find_all_of_tag(html: str, tag: str):
    opens = list(find_all(f"<{tag}", html))
    closes = list(find_all(f"</{tag}>", html))
    if len(opens) != len(closes):
        raise Exception("Huh?! Weird!")

    for o, c in zip(opens, closes):
        yield html[o:c]


def find_all(pattern, text):
    # inspired by: https://stackoverflow.com/a/34445090
    i = text.find(pattern)
    while i != -1:
        yield i
        i = text.find(pattern, i + 1)


def clean_str(text: str):
    return " ".join(str(text).split())


if __name__ == "__main__":
    main()
