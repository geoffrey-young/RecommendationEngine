# Project Source Data

This directory contains the initial data sources for this project.

| File | Description |
| -------------- | --- |
| **[`events.json.gz`](events.json.gz)** | The full set of event data for this project |
| **[`DMA-zip.csv.gz`](DMA-zip.csv.gz)** | A crosswalk of zipcode and DMA identifier, used to enrich event data |

Details for each data set follow.

#### Event Data

`events.json.gz` contains all the events to be included in this exercise.

Consider this file to be the master event data - the kind of data that a customer service representative might update but that you, as a developer, must consdier immutable.  Whatever transformations you will perform on the data will take the form of an enriched data set stored in another, more appropriate system.

In terms of data model, each record should be self-explanatory.  Here is a sample record:

```json
  {  
      "event_description" : "Rapid five-minute presentations, accompanied by 20 slides ticking down at 15-second intervals, inspire the crowd with ingenuity, humor, and imagination\u00e2\u0080\u0094ideas that are a call to action, that turn the past upside down, that point the way by which you help make a better future.\u00c2\u00a0\n\nNote: If you are wondering who is speaking, you are doing it wrong! Show up to be inspired by people you have never heard of... as well as some people you never thought you would run into at JB's.\n",   
      "event_end_utc" : "26 Oct 2018 02:00:00",
      "event_id" : "1ffcb624-c1d0-11e8-8ab2-22000a10f020",
      "event_name" : "Ignite Philly 21",
      "event_start_utc" : "25 Oct 2018 22:00:00",
      "facebook_event_id" : null,
      "hashtag" : null,
      "organization_id" : "ignitephilly",
      "organization_name" : "Ignite Philly",
      "tags" : [
         "ignitephilly"
      ],
      "venue_city" : "Philadelphia",
      "venue_name" : "Johnny Brenda's",
      "venue_state" : "PA",
      "venue_street" : "1201 N. Frankford Ave",
      "venue_timezone" : "US/Eastern",
      "venue_zip" : "19125"
   },
```

You can assume `event_id` is unique and that `organization_id` can be used as a foreign key for grouping events together by the host Organization.  Do not assume that all fields are always present or that their format is uniform.  For example, null fields may be `null`, `""`, or simply missing from the dat structure.

To give credit where credit is due, these events are real and come to you courtesy of TicketLeap and their public event API.  They were gleaned in a very polite manner, and have been sanitized slightly to remove URLs, images, and other fields not relevant to the exercise at hand.  Given that, please, please don't go out to TicketLeap and hammer their servers looking for more event details to improve your engine - all you need in terms of base event information is here, and it would be both bad form and bad karma to needlessly saturate their public API again just to end up with the same set of data.  Major points off if my friends at TicketLeap slack me about a surge in API activity.

#### DMA Data

`DMA-zip.csv.gz` is a crosswalk between DMAs, County, State and Zip Codes as of 2016, courtesy of the [Geographic Information on Designated Media Markets](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IVXEHT) archive in the [Harvard Dataverse](https://dataverse.harvard.edu/).

This map is an example of an external data source you would use to enrich existing base data.  For this project, you will be adding DMA codes and descriptions to each event record for use in your recommendation engine.
