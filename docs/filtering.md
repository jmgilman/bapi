# Filtering

The Beancount API seeks to maximize the versatility available in extracting data
from your beancount ledger. The endpoints are structured in a way to support
this, and, in addition, many endpoints offer the ability to further refine the
results produced.

## Filter

The first method available is through a [JMESPath][1] expression. Endpoints which
return a list of data can be further filtered by providing a filtering
expression. This allows, for example, to filter a response to only include
results which fall between certain dates:

```shell
curl http://localhost:8080/directive/?filter=[?date > 2022-01-01]
```

Note: Examplesa are not url-encoded for readability purposes

The above example would only return entries which have a date after 2022-01-01.
The syntax may be unfamiliar to those who have not used JMESPath, but more
information can be found in the [docs][2]. This query parameter provides
substantial more flexibility with controlling the results of a query and can
offload processing to the server and save on client bandwidth. Another example:

```shell
curl http://localhost:8080/directive/open
curl http://localhost:8080/directive/?filter=[?ty == `Open`]
```

The above two queries will produce identical results.

## Searching

In addition to filtering, some endpoints offer the ability to filter results by
performing a full-text search against textual data. For example, to find all
accounts which have the word `Assets` in it:

```shell
curl https://localhost:8080/account/?search=Assets
```

To find all transactions in which the word `Home Depot` appears in the narration
or payee fields:

```shell
curl https://localhost:8080/directive/transaction?search=Home Depot
```

In some cases, both the filter and search parameters can be used:

```shell
curl https://localhost:8080/directive/transaction?filter=[?date > 2022-01-01]&search=Home Depot
```

By default, the filter expression will be evaluated first and then the search
will be applied to the results from the filter. This behavior can be changed by
setting the `priority` query parameter:

```shell
curl https://localhost:8080/directive/transaction?filter=[?date > 2022-01-01]&search=Home Depot&priority=search
```

The above would run the search first and then filter the results from there.

[1]: https://jmespath.org/
[2]: https://jmespath.org/tutorial.html#filter-projections
