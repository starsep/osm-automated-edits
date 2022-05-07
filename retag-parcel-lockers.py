#!/usr/bin/env python3
from osm_bot_abstraction_layer.generic_bot_retagging import run_simple_retagging_task


OVERPASS_QUERY = """
[out:xml][timeout:25000];
area[name='Polska']->.searchArea;
(
  nwr["amenity"="vending_machine"]["vending"~"(parcel_pickup|parcel_mail_in)"](area.searchArea);
);
out body;
"""


def edit_element(tags):
    if tags["amenity"] != "vending_machine":
        return tags
    vending = tags["vending"]
    if not ("parcel_pickup" in vending or "parcel_mail_in" in vending):
        return tags
    if vending in {
        "parcel_pickup;parcel_mail_in",
        "parcel_pickup; parcel_mail_in",
        "parcel_mail_in;parcel_pickup",
    }:
        tags["amenity"] = "parcel_locker"
        del tags["vending"]
        tags["parcel_mail_in"] = "yes"
    elif vending == "parcel_pickup":
        tags["amenity"] = "parcel_locker"
        del tags["vending"]
    else:
        print(f"Unexpected vending={vending}")
    return tags


def main():
    run_simple_retagging_task(
        max_count_of_elements_in_one_changeset=500,
        objects_to_consider_query=OVERPASS_QUERY,
        objects_to_consider_query_storage_file="parcel_lockers.osm",
        is_in_manual_mode=False,
        changeset_comment="Zmiana tagowania paczkomatów z amenity=vending_machine na amenity=parcel_locker",
        discussion_url="https://forum.openstreetmap.org/viewtopic.php?id=74790",
        osm_wiki_documentation_page="https://wiki.openstreetmap.org/wiki/Mechanical_Edits/starsep-bot/retag_parcel_locker",
        edit_element_function=edit_element,
    )


if __name__ == "__main__":
    main()
