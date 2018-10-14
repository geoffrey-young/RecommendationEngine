# Let's Build a Recommendation Engine

<!-- toc -->

- [Introduction](#introduction)
- [The Project](#the-project)
- [Approach](#approach)
- [Phases](#phases)
  * [Phase 1: Pipeline](#phase-1-pipeline)
  * [Phase 2: Display](#phase-2-display)
  * [Phase 3: Enrichment](#phase-3-enrichment)
  * [Phase 4: Analysis](#phase-4-analysis)
  * [Phase 5: Iteration](#phase-5-iteration)
- [Deliverables](#deliverables)
  * [Phase 1: Pipeline](#phase-1-pipeline-1)
  * [Phase 2: Display](#phase-2-display-1)
  * [Phase 3: Enrichment](#phase-3-enrichment-1)
  * [Phase 4: Analysis](#phase-4-analysis-1)
  * [Phase 5: Iteration](#phase-5-iteration-1)
- [Background](#background)
- [Resources](#resources)
  * [Data](#data)
  * [Links](#links)

<!-- tocstop -->

### Introduction

Welcome to *Let's Build a Recommendation Engine*!

Whether you are aware of it or not, you are exposed to recommendation engines all the time.  Or at least the output of a recommendation engine, generally in the form of *"You might also like..."* suggestions on websites like Amazon, Netflix, and just about any other mainstream service.  Industry wide, companies spend millions and millions of dollars in the care and feeding of recommendation engines.  Why?  Because recommendations lead to increased revenue.  Lots of revenue.  So much so that back in 2006 Netflix created the [Netflix Prize](https://www.netflixprize.com/) and offered a cool **one million dollars** to the first person (or team) that could best the Netflix algorithm by more than 10%.  (Note: it took *3 years*).

Needless to say, some of the best minds in the world are working on various implementations of recommendation engines in a wide variety of problem spaces... and you are about to be one of them.

### The Project

In this project you will be creating a recommendation engine for an event ticketing system.

Starting from a set of [data](data/) consisting of 81,494 events (concerts, festivals, etc) and associated details from January 1, 2016 onward, you will be generating recommendations for a *"You might also be interested in..."* display on a website.  You will be responsible for designing and implementing a data processing pipeline, enriching the core data with additional data sets, designing recommendation algorithms, and the web application that displays the end results.


### Approach

Think of this as a proof of concept exercise you could be tasked with day one at a new job - you are handed a raw data set and expected to show off your work in a presentation to the head of Product Development after a few sprints.  This project, if worked through to completion, will prepare you for that day.

Heavy use of [Amazon Web Services](https://aws.amazon.com/) is strongly encouraged.  In fact, this entire project could be tackled using only the [AWS Always Free Tier](https://aws.amazon.com/free/?nc2=h_ql_pr&awsf.Free%20Tier%20Types=categories%23alwaysfree) via a clever combination of [Lambda](https://aws.amazon.com/lambda/), [Glue](https://aws.amazon.com/glue/), and [DynamoDB](https://aws.amazon.com/dynamodb/).  Other approaches using more idiomatic AWS tools and services will be suggested along the way.  In the end, however, you ought to explore and ultimately use whatever tools capture your interest and imagination.


### Phases

The project is broken up into several phases, each with its own deliverables.

   * Pipeline
   * Display
   * Enrichment
   * Analysis
   * Iteration

Note that the order of the phases is specific and intentional - while the Iteration phase is where you will spend the bulk of your time, both on this project and at your job, getting the proper scaffolding in place so you can iterate on your ideas quickly is the key to happiness and success.

#### Phase 1: Pipeline

While your mind is probably already spinning with all kinds of novel recommendation dimensions, the first step is actually to hunker down and figure out the mechanics of how you will munge your data.  We all tend to jump in to scripts on our laptops, but in the end the long-term total cost of ownership of that approach is expensive.  

This phase asks you to take a step back and construct a data pipeline to serve as the backbone of your project, the operational center where simply clicking a button will move your data through your algorithms with ease.  Lather, rinse, repeat.  It also includes using that pipeline for early-stage transforms such as data normalization and basic scrubbing.

While there are many different tools and technologies you could use, building your pipeline in AWS strongly encouraged.  A suggested approach is to:

   * Put your source data - `events.json.gz` - into S3
   * Create a Glue crawler for the source data in S3
   * Create a job in AWS Glue to read from S3 and output the results of your transformations as parquet files in S3
   * Create a Glue crawler for the transformed parquet data

I can speak from experience that, coming to AWS Glue cold, this can be accomplished in a day, troubleshooting and all.

A good place to start after [reading up on AWS Glue](https://aws.amazon.com/glue/getting-started/) is the [Data cleaning with AWS Glue](https://github.com/aws-samples/aws-glue-samples/blob/master/examples/data_cleaning_and_lambda.md) tutorial.  Another, more graphic example, is [Build a Data Lake Foundation with AWS Glue and Amazon S3](https://aws.amazon.com/blogs/big-data/build-a-data-lake-foundation-with-aws-glue-and-amazon-s3/).

It is worth noting that you need to create a custom JSON classifier for the Glue crawler due to the size of `events.json.gz` - see the solution [here](https://forums.aws.amazon.com/message.jspa?messageID=842705#842705).  Also, keep it in its compressed form in S3 - Glue seems to behave better.


#### Phase 2: Display

Now that you have both clean data and a repeatable way of generating it when it changes, it's time to build a way to peek into your results.  It may seem premature to focus on display now, but you are going to want to see the results of your recommendation algorithms as you experiment with them so taking care of the front end now will actually make your life easier in the long run.

Running a visualization from a big data tool like EMR, Hive, RedShift, etc is way too slow - these tools are great for data crunching, but once you have the results they belong in a metadata store for quick, easy access.  Therefore, the final step in your data pipeline should be to offload computed recommendations to a datastore that fits your use case.  For example, in a real application loading recommendations into Elasticsearch would not only allow for low-latency requests for display, but would also allow for faceting and filtering of results on demand.

Building on the AWS approach in Phase 1, the suggested approach is to

   * Use an AWS Lambda routine to load the transformed parquet files from Phase 1 to DynamoDB
   * Create a serverless web application with AWS API Gateway, Lambda, and DynamoDB.

A simple way to use Lambda to read from parquet is to use [AWS Athena](https://aws.amazon.com/athena/).  Assuming you created a Glue crawler for your parquet results the data should be immediately visible via Athena, making the task relatively straightforward.

A full tutorial on building a serverless web application can be found [here](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).  You don't need to worry about user authentication.

The display doesn't need to be anything fancy - remember, this is a PoC and you only have text to work with, so a simple, structure result page is fine.  Keep in mind that this page will also be used to display your recommendations in Phase 4.


#### Phase 3: Enrichment

Now we start getting to the fun part.

At this point, you should be able to go to a web page and see the data from `events.json.gz` for a single event.  It's time to show some recommendations along with it.

Whatever recommendations your amazing algorithms come up with, if the user lives in Philadelphia but your recommendation is in Wisconsin it's not going to be terribly useful.  With the base event data enriched with some basic [DMA](https://en.wikipedia.org/wiki/Media_market) information, we can map events to a geographic area and group them together.

The enrichment phase asks you to pull in DMA codes and descriptions from `DMA-zip.csv.gz` and add that data to each event record based on the venue zipcode.  The result of this enrichment will allow recommendations for an event in Media, PA to include events in Haddon Township, NJ but not in Boston, MA.

To continue building  the AWS Glue pipeline, you might

   * Put your source data - `DMA-zip.csv.gz` - into S3
   * Create a Glue crawler for the source data in S3
   * Create a new Glue job that reads the parquet transformations from Phase 1, applies the mapping, and outputs the mapped data to parquet
   * Create a Glue crawler for the transformed parquet data

If you followed this path, you would need to change your load routines to point to a Athena data source.  Another option is to make the Glue job from Phase 1 into a more monolithic codebase that does all your transformations and mappings.  Think about the benefits of each approach as you go.  Remember, the main cost of an application is in the maintainance not the development - how can you make your life easier as you add new logic and routines?

#### Phase 4: Analysis

At this point, you have an established framework for processing, enriching, and displaying data.  It's time to start coming up with some recommendations.

What makes for a good recommendation?  That is the question.  

With the addition of DMA data to your data set, you already have enough to show *"Other Events in Your Area..."* suggestions.  As it turns out, showing *any* recommendation is better than showing no recommendations, so your PoC project is adding value already!  We can do even more just with the event data we have on hand.

You have some basic event details to work with such as the name and description of the event.  Finding events with similar names and/or descriptions is a great place to start.

Once you can relate one event to another, start thinking about what storage and retrieval of that information is going to look like.  If you went with the DynamoDB solution to Phase 2, do you want to store recommendations separate from the base event data?

Given the small data set, event dates can be ignored as you find recommendations for suggestion - you wouldn't want to recommend past events in a real application (that would just make people feel bad they missed it) but for the purposes of this project don't worry about incorporating date logic.  Of course, if you wanted to you could, now that all your dates are standardized as a result of your Phase 1 data normalization.  How convenient.

#### Phase 5: Iteration

Now that you have some recommendation basics flowing, it's time to really put some thought into both expanding and refining recommendations.  It is far trickier than you might think.  For example:

   * Events at the same venue are a good idea... but will a person who just purchased tickets for a Friday night concert want to see that same show on Saturday?
   * Are people interested in their family reunion also interested in other family reunions?

Think about ways to enrich the data in order to come up with different recommendation dimensions.  For example:

   * Are people interested in wine festivals also interested in beer festivals?  How would you find out?
   * How do hashtags relate across events?  What data enrichment would help?
   * Are events a certain distance away more intersting that events in the same DMA?

There is no "best recommendation" or right answer, so explore the data and your ideas with gusto and see where they lead.


### Deliverables

Any and all underlying code should be checked in to GitHub in your fork of this repo.  For example, if you create a Python script for use in an AWS Glue job, check it in to `glue/scripts/`, a one-off script for fetching public data might go into `utils/`, etc.

Every Phase must include a diagram documenting your ecosystem - what components you are using, what scripts and routines are involved, etc.  You can start start with [this template](https://drive.google.com/file/d/1v3l9bKkw5MWRXFgzkYfLiFeNpNao7WN6/view?usp=sharing).

#### Phase 1: Pipeline

1. A transformation pipeline that cleans and normalizes incoming data.  Transformations *must* include:

   * Converting all dates to [ISO 8601 UTC datetime format](https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations) (YYYY-mm-dd**T**HH:MM:SS**Z**).*

   * Normalizing the data to remove extraneous characters (embedded newlines, non-renderable UTF-8 symbols, etc).

2. An exported PNG [draw.io](https://www.draw.io) diagram representing your pipeline.

3. A (merged and closed) pull request from your feature branch (`phase_1`) to your master that covers all your code, utilities, notes, and so on.

(*) If you start using this datetime format and stick to UTC now you'll be extremely thankful later on in your career.


#### Phase 2: Display

1. A display pipeline that takes the output of the Phase 1 transformations and loads them into a datastore.

2. A web-based display that can query the datastore and display results for a single, known event id.

3. An exported PNG [draw.io](https://www.draw.io) diagram representing your ecosystem, including Phase 1.

4. A (merged and closed) pull request from your feature branch (`phase_2`) to your master that covers all your code, utilities, notes, and so on.


#### Phase 3: Enrichment

1. A transformation pipeline that merges `DMA-zip.csv.gz` data with `events.json.gz`.

2. Display of the event's DMA name in your web application.

3. An exported PNG [draw.io](https://www.draw.io) diagram representing your ecosystem, including Phase 2.

4. A (merged and closed) pull request from your feature branch (`phase_3`) to your master that covers all your code, utilities, notes, and so on.


#### Phase 4: Analysis

1. A transformation pipeline that creates event recommendations based on at least one algorithm.

2. Display of recommendations on the web page alongside the requested event.  The display *must* include

   * At least 5 recommended events in the same geographic area
   * The event name, description, venue name and address (for visual human "relevancy scoring")
   * The reason for the recommendation, such as "Based on events in a similar location" or "Based on events with *wine* in their name"

3. An exported PNG [draw.io](https://www.draw.io) diagram representing your ecosystem, including Phase 3.

4. A (merged and closed) pull request from your feature branch (`phase_4`) to your master that covers all your code, utilities, notes, and so on.


#### Phase 5: Iteration

1. A transformation pipeline that creates event recommendations based on at least one additional enriched data set.

2. An exported PNG [draw.io](https://www.draw.io) diagram representing your entire ecosystem.

3. A (merged and closed) pull request from your feature branch (`phase_5`) to your master that covers all your code, utilities, notes, and so on.


### Background

This exercise was developed for the [CS 562: Big Data Algorithms](https://crab.rutgers.edu/~shende/cs562/index.html) course at Rutgers University Camden in the Fall 2018 term.  It was born out of conversations between me (Geoff) and Dr. [Sunil Shende](https://shende.camden.rutgers.edu/), the Graduate Program Director for the Rutgers [MS program in Scientific Computing](https://cs.camden.rutgers.edu/graduate/scientific-computing/).  Dr. Shende's MS program aims to prepare students for industry careers in engineering and data science, and I was asked if I could create a project that mirrored a real life problem.  To that end, this exercise is intended to be a challenging but straightforward project graduates could encounter upon entering the workforce.  One that asks a lot of them on many fronts - from pull requests to html to provisioning AWS services - in addition to the "real work" of data science algorithms.

Many thanks to Dr. Shende for the opportunity to work with him and his class.  Hopefully, everyone has fun with the experiment.


### Resources

#### Data

Initial data sets can be found in the [`data/`](data/) directory in this repo

   * [`events.json.gz`](data/events.json.gz)
   * [`DMA-zip.csv.gz`](data/DMA-zip.csv.gz)

plus whatever other data sources you can dream up.


#### Links

   * [Amazon Web Services](https://aws.amazon.com/)
   * [AWS Glue](https://aws.amazon.com/glue/)
   * [AWS Lambda](https://aws.amazon.com/lambda/)
   * [AWS API Gateway](https://aws.amazon.com/api-gateway/)
   * [AWS Athena](https://aws.amazon.com/athena/)
   * [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
   * [draw.io](https://www.draw.io)
   * [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
   * [DMA background](https://en.wikipedia.org/wiki/Media_market)
   * [`DMA_zip.csv` source data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IVXEHT)
