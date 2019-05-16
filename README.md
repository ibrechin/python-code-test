# Starship Listing API

This API allows for the creation of starship sale listings. The root of the API is at `/api/` - if you request this path it will return the available endpoints. You can also explore the API using a web browser.

# Endpoints

## Starships

The starship endpoint `/api/starships/` lists the available ship types and their IDs. You will need the ID of the relevant ship type when creating a listing.

## Listings

The listings API allows for the creation and retrieval of sale listings. To create a listing, make a POST to `/api/listings/` with the fields `name`, `price` and `ship_type`. `ship_type` should be the ID of an existing starship.

Listings can be retrieved by a GET request to `/api/listings/`. You can use query parameters to order and filter the returned list. You can filter by `starship_class` and `active` status.

e.g. to filter by `starship_class`:

```
/api/listings/?starship_class=cruiser
```

You can also order by `price` or `last_listed` using the `ordering` parameter.

e.g. to order by `price`:

```
/api/listings/?ordering=price
```

### Activating and deactivating listings

You can activate and deactivate a listing by POSTing to the relevant action endpoints.

e.g. to deactivate listing with ID 1, POST to:

```
/api/listings/1/deactivate/
```

and to reactivate:

```
/api/listings/1/activate/
```

The `last_listed` timestamp is updated when a listing is reactivated. It is recommended that when retrieving listings for display, you should filter them with `active=true`.
