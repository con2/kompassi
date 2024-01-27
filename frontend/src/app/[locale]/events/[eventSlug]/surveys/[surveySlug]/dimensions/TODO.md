# Intercepting routes may be too heavy machinery for the dimension editor

The new dimension / edit dimension modal was written using an intercepting route. This allows both opening it as a modal on top of the dimensions view and navigating to it as a stand-alone view.

While a fun exercise in intercepting routes, this may not be very useful or necessary for the actual use case.

## On a hard reload, can we open the dimensions page and then the modal on top of it

…without resorting to some `?intent=createValue(dimensionSlug)` that redirects to the intercepting route?

For example: The user navigates to `/event/hitpoint2024/surveys/larp-survey/dimensions/new`. Instead of opening the form as a standalone page, could we make it open the dimensions view and then the modal on top of it, so that the Next.js recommended way of closing the modal with `router.back()` would work.

## Check if the @modal can be pushed to root layout

If we settle on using intercepting routes, there are still things we could do

It's a bit unwieldy to have to create the layout containing a `@modal` slot, with its own `default.tsx`, in every page that happens to use modals via intercepting routes. See if it would be possible to move the `@modal` slot to the root layout.

## See also

- [Next.js documentation: Intercepting routes](https://nextjs.org/docs/app/building-your-application/routing/intercepting-routes)
