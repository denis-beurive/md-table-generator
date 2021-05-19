# Description

This script generates nice looking MD tables.

# Usage

## Command line

    $ python md2table.py -h
    usage: md2table.py [-h] [--verbose] [--sep SEP] input [captions [captions ...]]
    
    MD table builder
    
    positional arguments:
      input       path to the input file
      captions    captions (a list of space separated labels)
    
    optional arguments:
      -h, --help  show this help message and exit
      --verbose   verbosity flag
      --sep SEP   field separator

## Example 1

Input file (`test.txt`):

    | TCP | 5672 | RabbitMQ | [web](https://www.rabbitmq.com/)
    | TCP | 9092 | Apache Kafka
    | TCP | 61616 | Apache Activemq
    | UDP

Command:

    python md2table.py test.txt protocol "port number" name link

Result:

    | protocol | port number | name            | link                             | 
    |----------|-------------|-----------------|----------------------------------|
    | TCP      | 5672        | RabbitMQ        | [web](https://www.rabbitmq.com/) |
    | TCP      | 9092        | Apache Kafka    |                                  |
    | TCP      | 61616       | Apache Activemq |                                  |
    | UDP      |             |                 |                                  |


# Example 2

You don't specify any captions.

Input file (`test.txt`):

    | TCP | 5672 | RabbitMQ | [web](https://www.rabbitmq.com/)
    | TCP | 9092 | Apache Kafka
    | TCP | 61616 | Apache Activemq
    | UDP

Command:

    python md2table.py test.txt

Result:

    |     |       |                 |                                  | 
    |-----|-------|-----------------|----------------------------------|
    | TCP | 5672  | RabbitMQ        | [web](https://www.rabbitmq.com/) |
    | TCP | 9092  | Apache Kafka    |                                  |
    | TCP | 61616 | Apache Activemq |                                  |
    | UDP |       |                 |                                  |

# Example 3

Use the "," as field separator (instead of "|").

Input file:

    , TCP , 5672 , RabbitMQ , [web](https://www.rabbitmq.com/)
    , TCP , 9092 , Apache Kafka
    , TCP , 61616 , Apache Activemq
    , UDP

Command:

    python md2table.py --sep=","  test.txt protocol "port number" name link

Result:

    | protocol | port number | name            | link                             | 
    |----------|-------------|-----------------|----------------------------------|
    | TCP      | 5672        | RabbitMQ        | [web](https://www.rabbitmq.com/) |
    | TCP      | 9092        | Apache Kafka    |                                  |
    | TCP      | 61616       | Apache Activemq |                                  |
    | UDP      |             |                 |                                  |
