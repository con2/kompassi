/* eslint-disable */
import * as types from './graphql';
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 */
const documents = {
    "\n  mutation CreateSurveyResponse($input: CreateSurveyResponseInput!) {\n    createSurveyResponse(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n": types.CreateSurveyResponseDocument,
    "\n  mutation InitFileUploadMutation($input: InitFileUploadInput!) {\n    initFileUpload(input: $input) {\n      uploadUrl\n      fileUrl\n    }\n  }\n": types.InitFileUploadMutationDocument,
    "\n  query SurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    profile {\n      displayName\n      email\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: null) {\n          loginRequired\n          anonymity\n          maxResponsesPerUser\n          countResponsesByCurrentUser\n          isActive\n\n          form(lang: $locale) {\n            language\n            title\n            description\n            fields\n          }\n\n          languages {\n            language\n          }\n        }\n      }\n    }\n  }\n": types.SurveyPageQueryDocument,
    "\n  query SurveyThankYouPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n": types.SurveyThankYouPageQueryDocument,
    "\n  mutation ResendOrderConfirmation($input: ResendOrderConfirmationInput!) {\n    resendOrderConfirmation(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n": types.ResendOrderConfirmationDocument,
    "\n  mutation UpdateOrder($input: UpdateOrderInput!) {\n    updateOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n": types.UpdateOrderDocument,
    "\n  mutation CancelAndRefundOrder($input: CancelAndRefundOrderInput!) {\n    cancelAndRefundOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n": types.CancelAndRefundOrderDocument,
    "\n  fragment AdminOrderPaymentStamp on LimitedPaymentStampType {\n    id\n    createdAt\n    correlationId\n    provider\n    type\n    status\n    data\n  }\n": types.AdminOrderPaymentStampFragmentDoc,
    "\n  fragment AdminOrderReceipt on LimitedReceiptType {\n    correlationId\n    createdAt\n    email\n    type\n    status\n  }\n": types.AdminOrderReceiptFragmentDoc,
    "\n  fragment AdminOrderCode on LimitedCodeType {\n    code\n    literateCode\n    status\n    usedOn\n    productText\n  }\n": types.AdminOrderCodeFragmentDoc,
    "\n  query AdminOrderDetail($eventSlug: String!, $orderId: String!) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      tickets {\n        order(id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          firstName\n          lastName\n          email\n          phone\n          canRefund\n          products {\n            title\n            quantity\n            price\n          }\n          paymentStamps {\n            ...AdminOrderPaymentStamp\n          }\n          receipts {\n            ...AdminOrderReceipt\n          }\n          codes {\n            ...AdminOrderCode\n          }\n        }\n      }\n    }\n  }\n": types.AdminOrderDetailDocument,
    "\n  fragment OrderList on FullOrderType {\n    id\n    formattedOrderNumber\n    displayName\n    email\n    createdAt\n    totalPrice\n    status\n  }\n": types.OrderListFragmentDoc,
    "\n  fragment ProductChoice on FullProductType {\n    id\n    title\n  }\n": types.ProductChoiceFragmentDoc,
    "\n  query OrderList(\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $searchTerm: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductChoice\n        }\n\n        orders(filters: $filters, search: $searchTerm) {\n          ...OrderList\n        }\n      }\n    }\n  }\n": types.OrderListDocument,
    "\n  mutation UpdateProduct($input: UpdateProductInput!) {\n    updateProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n": types.UpdateProductDocument,
    "\n  mutation DeleteProduct($input: DeleteProductInput!) {\n    deleteProduct(input: $input) {\n      id\n    }\n  }\n": types.DeleteProductDocument,
    "\n  fragment AdminProductOldVersion on LimitedProductType {\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n  }\n": types.AdminProductOldVersionFragmentDoc,
    "\n  fragment AdminProductDetail on FullProductType {\n    id\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n    availableFrom\n    availableUntil\n    canDelete\n\n    quotas {\n      id\n    }\n\n    supersededBy {\n      id\n    }\n\n    oldVersions {\n      ...AdminProductOldVersion\n    }\n  }\n": types.AdminProductDetailFragmentDoc,
    "\n  query AdminProductDetailPage($eventSlug: String!, $productId: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          id\n          name\n          countTotal\n        }\n\n        product(id: $productId) {\n          ...AdminProductDetail\n        }\n      }\n    }\n  }\n": types.AdminProductDetailPageDocument,
    "\n  mutation CreateProduct($input: CreateProductInput!) {\n    createProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n": types.CreateProductDocument,
    "\n  mutation ReorderProducts($input: ReorderProductsInput!) {\n    reorderProducts(input: $input) {\n      products {\n        id\n      }\n    }\n  }\n": types.ReorderProductsDocument,
    "\n  fragment ProductList on FullProductType {\n    id\n    title\n    description\n    price\n    isAvailable\n    availableFrom\n    availableUntil\n    countPaid\n    countReserved\n    countAvailable\n  }\n": types.ProductListFragmentDoc,
    "\n  query ProductList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductList\n        }\n      }\n    }\n  }\n": types.ProductListDocument,
    "\n  mutation UpdateProgramBasicInfo($input: UpdateProgramInput!) {\n    updateProgram(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n": types.UpdateProgramBasicInfoDocument,
    "\n  mutation UpdateProgramDimensions($input: UpdateProgramDimensionsInput!) {\n    updateProgramDimensions(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n": types.UpdateProgramDimensionsDocument,
    "\n  query ProgramAdminDetailDimensionsQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      program {\n        dimensions {\n          ...DimensionRowGroup\n        }\n\n        program(slug: $programSlug) {\n          slug\n          title\n          cachedDimensions\n        }\n      }\n    }\n  }\n": types.ProgramAdminDetailDimensionsQueryDocument,
    "\n  query ProgramAdminDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          slug\n          title\n          description\n          cachedHosts\n\n          programOffer {\n            id\n            values\n          }\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n": types.ProgramAdminDetailQueryDocument,
    "\n  fragment ProgramAdmin on FullProgramType {\n    slug\n    title\n    scheduleItems {\n      startTime\n    }\n    cachedDimensions\n  }\n": types.ProgramAdminFragmentDoc,
    "\n  query ProgramAdminList(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        # TODO fragmentify\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isKeyDimension\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        programs(filters: $filters) {\n          ...ProgramAdmin\n        }\n      }\n    }\n  }\n": types.ProgramAdminListDocument,
    "\n  mutation PutProgramDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n": types.PutProgramDimensionDocument,
    "\n  mutation DeleteProgramDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n": types.DeleteProgramDimensionDocument,
    "\n  mutation PutProgramDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n": types.PutProgramDimensionValueDocument,
    "\n  mutation DeleteProgramDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n": types.DeleteProgramDimensionValueDocument,
    "\n  query ProgramDimensionsList($eventSlug: String!, $locale: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        dimensions(publicOnly: false) {\n          ...DimensionRowGroup\n        }\n      }\n    }\n  }\n": types.ProgramDimensionsListDocument,
    "\n  mutation UpdateProgramFormLanguage($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.UpdateProgramFormLanguageDocument,
    "\n  mutation DeleteProgramFormLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n": types.DeleteProgramFormLanguageDocument,
    "\n  mutation UpdateFormFieldsMutation($input: UpdateFormFieldsInput!) {\n    updateFormFields(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.UpdateFormFieldsMutationDocument,
    "\n  mutation PromoteProgramFormFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.PromoteProgramFormFieldToDimensionDocument,
    "\n  query EditProgramFormFieldsPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n": types.EditProgramFormFieldsPageDocument,
    "\n  fragment EditProgramFormLanguage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n": types.EditProgramFormLanguageFragmentDoc,
    "\n  query EditProgramFormLanguagePage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramFormLanguage\n        }\n      }\n    }\n  }\n": types.EditProgramFormLanguagePageDocument,
    "\n  mutation CreateProgramFormLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n": types.CreateProgramFormLanguageDocument,
    "\n  mutation UpdateProgramFormMutation($input: UpdateSurveyInput!) {\n    updateProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.UpdateProgramFormMutationDocument,
    "\n  mutation DeleteProrgamFormMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n": types.DeleteProrgamFormMutationDocument,
    "\n  fragment EditProgramForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    activeFrom\n    activeUntil\n    canRemove\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n": types.EditProgramFormFragmentDoc,
    "\n  query EditProgramFormPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramForm\n        }\n      }\n    }\n  }\n": types.EditProgramFormPageDocument,
    "\n  mutation CreateProgramForm($input: CreateProgramFormInput!) {\n    createProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.CreateProgramFormDocument,
    "\n  fragment OfferForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n": types.OfferFormFragmentDoc,
    "\n  query ProgramFormsPage($eventSlug: String!, $locale: String) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      forms {\n        surveys(includeInactive: true, app: PROGRAM_V2) {\n          ...OfferForm\n        }\n      }\n    }\n  }\n": types.ProgramFormsPageDocument,
    "\n  mutation AcceptProgramOffer($input: AcceptProgramOfferInput!) {\n    acceptProgramOffer(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n": types.AcceptProgramOfferDocument,
    "\n  fragment ProgramOfferDetail on FullResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n      email\n    }\n    language\n    values\n    form {\n      fields\n      survey {\n        title(lang: $locale)\n        slug\n      }\n    }\n    programs {\n      slug\n      title\n    }\n    cachedDimensions\n  }\n": types.ProgramOfferDetailFragmentDoc,
    "\n  query ProgramOfferPage(\n    $eventSlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      program {\n        dimensions(publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isTechnical\n          isMultiValue\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n          }\n        }\n\n        programOffer(id: $responseId) {\n          ...ProgramOfferDetail\n        }\n      }\n    }\n  }\n": types.ProgramOfferPageDocument,
    "\n  fragment ProgramOffer on FullResponseType {\n    id\n    createdAt\n    createdBy {\n      displayName\n    }\n    sequenceNumber\n    values(keyFieldsOnly: true)\n    form {\n      survey {\n        title(lang: $locale)\n      }\n      language\n    }\n    cachedDimensions\n    programs {\n      slug\n      title\n    }\n  }\n": types.ProgramOfferFragmentDoc,
    "\n  fragment ProgramOfferDimension on FullDimensionType {\n    slug\n    title(lang: $locale)\n    isKeyDimension\n    isTechnical\n\n    values(lang: $locale) {\n      slug\n      title(lang: $locale)\n      color\n      isTechnical\n    }\n  }\n": types.ProgramOfferDimensionFragmentDoc,
    "\n  query ProgramOffers(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        stateDimension {\n          ...ProgramOfferDimension\n        }\n\n        countProgramOffers\n        programOffers(filters: $filters) {\n          ...ProgramOffer\n        }\n      }\n    }\n  }\n": types.ProgramOffersDocument,
    "\n  mutation MarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    markScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n": types.MarkScheduleItemAsFavoriteDocument,
    "\n  mutation UnmarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    unmarkScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n": types.UnmarkScheduleItemAsFavoriteDocument,
    "\n  fragment ScheduleProgram on LimitedProgramType {\n    slug\n    title\n    cachedDimensions\n    color\n  }\n": types.ScheduleProgramFragmentDoc,
    "\n  fragment ScheduleItemList on FullScheduleItemType {\n    slug\n    location\n    subtitle\n    startTime\n    endTime\n    program {\n      ...ScheduleProgram\n    }\n  }\n": types.ScheduleItemListFragmentDoc,
    "\n  query ProgramListQuery(\n    $locale: String\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $hidePast: Boolean\n  ) {\n    profile {\n      program {\n        scheduleItems(\n          eventSlug: $eventSlug\n          filters: $filters\n          hidePast: $hidePast\n        ) {\n          ...ScheduleItemList\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        listFilters: dimensions(isListFilter: true) {\n          slug\n          title(lang: $locale)\n          isListFilter\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        scheduleItems(filters: $filters, hidePast: $hidePast) {\n          ...ScheduleItemList\n        }\n      }\n    }\n  }\n": types.ProgramListQueryDocument,
    "\n  mutation CreateFeedback($input: ProgramFeedbackInput!) {\n    createProgramFeedback(input: $input) {\n      success\n    }\n  }\n": types.CreateFeedbackDocument,
    "\n  query ProgramFeedbackQuery($eventSlug: String!, $programSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        program(slug: $programSlug) {\n          title\n          isAcceptingFeedback\n        }\n      }\n    }\n  }\n": types.ProgramFeedbackQueryDocument,
    "\n  fragment ProgramDetailAnnotation on ProgramAnnotationType {\n    annotation {\n      slug\n      type\n      title(lang: $locale)\n    }\n    value(lang: $locale)\n  }\n": types.ProgramDetailAnnotationFragmentDoc,
    "\n  query ProgramDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    profile {\n      program {\n        scheduleItems(eventSlug: $eventSlug) {\n          slug\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          title\n          description\n          cachedHosts\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n": types.ProgramDetailQueryDocument,
    "\n  mutation UpdateQuota($input: UpdateQuotaInput!) {\n    updateQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n": types.UpdateQuotaDocument,
    "\n  mutation DeleteQuota($input: DeleteQuotaInput!) {\n    deleteQuota(input: $input) {\n      id\n    }\n  }\n": types.DeleteQuotaDocument,
    "\n  fragment QuotaProduct on LimitedProductType {\n    id\n    title\n    price\n    countReserved\n  }\n": types.QuotaProductFragmentDoc,
    "\n  query AdminQuotaDetailPage($eventSlug: String!, $quotaId: Int!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quota(id: $quotaId) {\n          id\n          name\n          countReserved\n          quota: countTotal\n          canDelete\n\n          products {\n            ...QuotaProduct\n          }\n        }\n      }\n    }\n  }\n": types.AdminQuotaDetailPageDocument,
    "\n  mutation CreateQuota($input: CreateQuotaInput!) {\n    createQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n": types.CreateQuotaDocument,
    "\n  fragment QuotaList on FullQuotaType {\n    id\n    title: name\n    countPaid\n    countReserved\n    countAvailable\n    countTotal\n  }\n": types.QuotaListFragmentDoc,
    "\n  query QuotaList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          ...QuotaList\n        }\n      }\n    }\n  }\n": types.QuotaListDocument,
    "\n  mutation PutSurveyDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n": types.PutSurveyDimensionDocument,
    "\n  mutation DeleteSurveyDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n": types.DeleteSurveyDimensionDocument,
    "\n  mutation PutSurveyDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n": types.PutSurveyDimensionValueDocument,
    "\n  mutation DeleteSurveyDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n": types.DeleteSurveyDimensionValueDocument,
    "\n  fragment ValueFields on DimensionValueType {\n    slug\n    color\n    isInitial\n    isTechnical\n    canRemove\n    title(lang: $locale)\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n  }\n": types.ValueFieldsFragmentDoc,
    "\n  fragment DimensionRowGroup on FullDimensionType {\n    slug\n    canRemove\n    title(lang: $locale)\n    isPublic\n    isKeyDimension\n    isMultiValue\n    isListFilter\n    isShownInDetail\n    isNegativeSelection\n    isTechnical\n    valueOrdering\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n    values {\n      ...ValueFields\n    }\n  }\n": types.DimensionRowGroupFragmentDoc,
    "\n  query DimensionsList(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String!\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          canRemove\n          languages {\n            language\n          }\n          dimensions {\n            ...DimensionRowGroup\n          }\n        }\n      }\n    }\n  }\n": types.DimensionsListDocument,
    "\n  mutation UpdateFormMutation($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.UpdateFormMutationDocument,
    "\n  mutation DeleteSurveyLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n": types.DeleteSurveyLanguageDocument,
    "\n  mutation PromoteSurveyFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.PromoteSurveyFieldToDimensionDocument,
    "\n  fragment EditSurveyFieldsPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    dimensions {\n      ...DimensionRowGroup\n    }\n\n    form(lang: $language) {\n      title\n      language\n      fields(enrich: false)\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n": types.EditSurveyFieldsPageFragmentDoc,
    "\n  query EditSurveyFieldsPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n": types.EditSurveyFieldsPageQueryDocument,
    "\n  fragment EditFormLanguagePage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n": types.EditFormLanguagePageFragmentDoc,
    "\n  query EditFormLanguagePageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditFormLanguagePage\n        }\n      }\n    }\n  }\n": types.EditFormLanguagePageQueryDocument,
    "\n  mutation CreateSurveyLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n": types.CreateSurveyLanguageDocument,
    "\n  mutation UpdateSurveyMutation($input: UpdateSurveyInput!) {\n    updateSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.UpdateSurveyMutationDocument,
    "\n  mutation DeleteSurveyMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n": types.DeleteSurveyMutationDocument,
    "\n  fragment EditSurveyPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    loginRequired\n    anonymity\n    maxResponsesPerUser\n    countResponsesByCurrentUser\n    activeFrom\n    activeUntil\n    canRemove\n    protectResponses\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n": types.EditSurveyPageFragmentDoc,
    "\n  query EditSurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditSurveyPage\n        }\n      }\n    }\n  }\n": types.EditSurveyPageQueryDocument,
    "\n  mutation UpdateResponseDimensions($input: UpdateResponseDimensionsInput!) {\n    updateResponseDimensions(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n": types.UpdateResponseDimensionsDocument,
    "\n  query SurveyResponseDetail(\n    $eventSlug: String!\n    $surveySlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n          anonymity\n          canRemoveResponses\n          protectResponses\n\n          dimensions {\n            title(lang: $locale)\n            slug\n            isTechnical\n            isMultiValue\n\n            values {\n              title(lang: $locale)\n              slug\n              color\n            }\n          }\n\n          response(id: $responseId) {\n            id\n            sequenceNumber\n            createdAt\n            createdBy {\n              displayName\n              email\n            }\n            language\n            values\n            form {\n              fields\n            }\n            cachedDimensions\n          }\n        }\n      }\n    }\n  }\n": types.SurveyResponseDetailDocument,
    "\n  mutation SubscribeToSurveyResponses($input: SubscriptionInput!) {\n    subscribeToSurveyResponses(input: $input) {\n      success\n    }\n  }\n": types.SubscribeToSurveyResponsesDocument,
    "\n  mutation UnsubscribeFromSurveyResponses($input: SubscriptionInput!) {\n    unsubscribeFromSurveyResponses(input: $input) {\n      success\n    }\n  }\n": types.UnsubscribeFromSurveyResponsesDocument,
    "\n  mutation DeleteSurveyResponses($input: DeleteSurveyResponsesInput!) {\n    deleteSurveyResponses(input: $input) {\n      countDeleted\n    }\n  }\n": types.DeleteSurveyResponsesDocument,
    "\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n    }\n    language\n    values(keyFieldsOnly: true)\n    cachedDimensions(keyDimensionsOnly: true)\n  }\n": types.SurveyResponseFragmentDoc,
    "\n  query FormResponses(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    profile {\n      forms {\n        surveys(eventSlug: $eventSlug, relation: SUBSCRIBED) {\n          slug\n        }\n      }\n    }\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          anonymity\n\n          fields(lang: $locale, keyFieldsOnly: true)\n          dimensions {\n            slug\n            title(lang: $locale)\n            isKeyDimension\n\n            values {\n              slug\n              title(lang: $locale)\n              color\n            }\n          }\n\n          countResponses\n          canRemoveResponses\n          protectResponses\n\n          responses(filters: $filters) {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n": types.FormResponsesDocument,
    "\n  query SurveySummary(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          fields(lang: $locale)\n          summary(filters: $filters)\n          countFilteredResponses: countResponses(filters: $filters)\n          countResponses\n          dimensions {\n            slug\n            title(lang: $locale)\n            values {\n              slug\n              title(lang: $locale)\n            }\n          }\n        }\n      }\n    }\n  }\n": types.SurveySummaryDocument,
    "\n  mutation CreateSurvey($input: CreateSurveyInput!) {\n    createSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n": types.CreateSurveyDocument,
    "\n  fragment Survey on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n": types.SurveyFragmentDoc,
    "\n  query Surveys($eventSlug: String!, $locale: String) {\n    profile {\n      forms {\n        surveys(relation: ACCESSIBLE) {\n          event {\n            slug\n            name\n          }\n          slug\n          title(lang: $locale)\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys(includeInactive: true, app: FORMS) {\n          ...Survey\n        }\n      }\n    }\n  }\n": types.SurveysDocument,
    "\n  mutation GenerateKeyPair($password: String!) {\n    generateKeyPair(password: $password) {\n      id\n    }\n  }\n": types.GenerateKeyPairDocument,
    "\n  mutation RevokeKeyPair($id: String!) {\n    revokeKeyPair(id: $id) {\n      id\n    }\n  }\n": types.RevokeKeyPairDocument,
    "\n  fragment ProfileEncryptionKeys on KeyPairType {\n    id\n    createdAt\n  }\n": types.ProfileEncryptionKeysFragmentDoc,
    "\n  query ProfileEncryptionKeys {\n    profile {\n      keypairs {\n        ...ProfileEncryptionKeys\n      }\n    }\n  }\n": types.ProfileEncryptionKeysDocument,
    "\n  query ProfileOrderDetail($eventSlug: String!, $orderId: String!) {\n    profile {\n      tickets {\n        order(eventSlug: $eventSlug, id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          canPay\n          products {\n            title\n            quantity\n            price\n          }\n\n          event {\n            slug\n            name\n          }\n        }\n      }\n    }\n  }\n": types.ProfileOrderDetailDocument,
    "\n  mutation ConfirmEmail($input: ConfirmEmailInput!) {\n    confirmEmail(input: $input) {\n      user {\n        email\n      }\n    }\n  }\n": types.ConfirmEmailDocument,
    "\n  fragment ProfileOrder on ProfileOrderType {\n    id\n    formattedOrderNumber\n    createdAt\n    totalPrice\n    status\n    eticketsLink\n    canPay\n\n    event {\n      slug\n      name\n    }\n  }\n": types.ProfileOrderFragmentDoc,
    "\n  query ProfileOrders {\n    profile {\n      tickets {\n        orders {\n          ...ProfileOrder\n        }\n\n        haveUnlinkedOrders\n      }\n    }\n  }\n": types.ProfileOrdersDocument,
    "\n  query ProfileSurveyResponsePage($locale: String!, $responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n\n          dimensions {\n            ...DimensionBadge\n          }\n\n          form {\n            title\n            language\n            fields\n            event {\n              slug\n              name\n            }\n            survey {\n              anonymity\n            }\n          }\n        }\n      }\n    }\n  }\n": types.ProfileSurveyResponsePageDocument,
    "\n  fragment ProfileResponsesTableRow on ProfileResponseType {\n    id\n    createdAt\n    dimensions(keyDimensionsOnly: true) {\n      dimension {\n        slug\n        title(lang: $locale)\n      }\n\n      value {\n        slug\n        title(lang: $locale)\n        color\n      }\n    }\n    form {\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n": types.ProfileResponsesTableRowFragmentDoc,
    "\n  query OwnFormResponses($locale: String!) {\n    profile {\n      forms {\n        responses {\n          ...ProfileResponsesTableRow\n        }\n      }\n    }\n  }\n": types.OwnFormResponsesDocument,
    "\n  fragment DimensionBadge on ResponseDimensionValueType {\n    dimension {\n      slug\n      title(lang: $locale)\n    }\n\n    value {\n      slug\n      title(lang: $locale)\n      color\n    }\n  }\n": types.DimensionBadgeFragmentDoc,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = graphql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function graphql(source: string): unknown;

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateSurveyResponse($input: CreateSurveyResponseInput!) {\n    createSurveyResponse(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateSurveyResponse($input: CreateSurveyResponseInput!) {\n    createSurveyResponse(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation InitFileUploadMutation($input: InitFileUploadInput!) {\n    initFileUpload(input: $input) {\n      uploadUrl\n      fileUrl\n    }\n  }\n"): (typeof documents)["\n  mutation InitFileUploadMutation($input: InitFileUploadInput!) {\n    initFileUpload(input: $input) {\n      uploadUrl\n      fileUrl\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query SurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    profile {\n      displayName\n      email\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: null) {\n          loginRequired\n          anonymity\n          maxResponsesPerUser\n          countResponsesByCurrentUser\n          isActive\n\n          form(lang: $locale) {\n            language\n            title\n            description\n            fields\n          }\n\n          languages {\n            language\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    profile {\n      displayName\n      email\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: null) {\n          loginRequired\n          anonymity\n          maxResponsesPerUser\n          countResponsesByCurrentUser\n          isActive\n\n          form(lang: $locale) {\n            language\n            title\n            description\n            fields\n          }\n\n          languages {\n            language\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query SurveyThankYouPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyThankYouPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          form(lang: $locale) {\n            title\n            thankYouMessage\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation ResendOrderConfirmation($input: ResendOrderConfirmationInput!) {\n    resendOrderConfirmation(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation ResendOrderConfirmation($input: ResendOrderConfirmationInput!) {\n    resendOrderConfirmation(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateOrder($input: UpdateOrderInput!) {\n    updateOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateOrder($input: UpdateOrderInput!) {\n    updateOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CancelAndRefundOrder($input: CancelAndRefundOrderInput!) {\n    cancelAndRefundOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CancelAndRefundOrder($input: CancelAndRefundOrderInput!) {\n    cancelAndRefundOrder(input: $input) {\n      order {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment AdminOrderPaymentStamp on LimitedPaymentStampType {\n    id\n    createdAt\n    correlationId\n    provider\n    type\n    status\n    data\n  }\n"): (typeof documents)["\n  fragment AdminOrderPaymentStamp on LimitedPaymentStampType {\n    id\n    createdAt\n    correlationId\n    provider\n    type\n    status\n    data\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment AdminOrderReceipt on LimitedReceiptType {\n    correlationId\n    createdAt\n    email\n    type\n    status\n  }\n"): (typeof documents)["\n  fragment AdminOrderReceipt on LimitedReceiptType {\n    correlationId\n    createdAt\n    email\n    type\n    status\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment AdminOrderCode on LimitedCodeType {\n    code\n    literateCode\n    status\n    usedOn\n    productText\n  }\n"): (typeof documents)["\n  fragment AdminOrderCode on LimitedCodeType {\n    code\n    literateCode\n    status\n    usedOn\n    productText\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query AdminOrderDetail($eventSlug: String!, $orderId: String!) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      tickets {\n        order(id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          firstName\n          lastName\n          email\n          phone\n          canRefund\n          products {\n            title\n            quantity\n            price\n          }\n          paymentStamps {\n            ...AdminOrderPaymentStamp\n          }\n          receipts {\n            ...AdminOrderReceipt\n          }\n          codes {\n            ...AdminOrderCode\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query AdminOrderDetail($eventSlug: String!, $orderId: String!) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      tickets {\n        order(id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          firstName\n          lastName\n          email\n          phone\n          canRefund\n          products {\n            title\n            quantity\n            price\n          }\n          paymentStamps {\n            ...AdminOrderPaymentStamp\n          }\n          receipts {\n            ...AdminOrderReceipt\n          }\n          codes {\n            ...AdminOrderCode\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment OrderList on FullOrderType {\n    id\n    formattedOrderNumber\n    displayName\n    email\n    createdAt\n    totalPrice\n    status\n  }\n"): (typeof documents)["\n  fragment OrderList on FullOrderType {\n    id\n    formattedOrderNumber\n    displayName\n    email\n    createdAt\n    totalPrice\n    status\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProductChoice on FullProductType {\n    id\n    title\n  }\n"): (typeof documents)["\n  fragment ProductChoice on FullProductType {\n    id\n    title\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query OrderList(\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $searchTerm: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductChoice\n        }\n\n        orders(filters: $filters, search: $searchTerm) {\n          ...OrderList\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query OrderList(\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $searchTerm: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductChoice\n        }\n\n        orders(filters: $filters, search: $searchTerm) {\n          ...OrderList\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateProduct($input: UpdateProductInput!) {\n    updateProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateProduct($input: UpdateProductInput!) {\n    updateProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteProduct($input: DeleteProductInput!) {\n    deleteProduct(input: $input) {\n      id\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteProduct($input: DeleteProductInput!) {\n    deleteProduct(input: $input) {\n      id\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment AdminProductOldVersion on LimitedProductType {\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n  }\n"): (typeof documents)["\n  fragment AdminProductOldVersion on LimitedProductType {\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment AdminProductDetail on FullProductType {\n    id\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n    availableFrom\n    availableUntil\n    canDelete\n\n    quotas {\n      id\n    }\n\n    supersededBy {\n      id\n    }\n\n    oldVersions {\n      ...AdminProductOldVersion\n    }\n  }\n"): (typeof documents)["\n  fragment AdminProductDetail on FullProductType {\n    id\n    createdAt\n    title\n    description\n    price\n    eticketsPerProduct\n    maxPerOrder\n    availableFrom\n    availableUntil\n    canDelete\n\n    quotas {\n      id\n    }\n\n    supersededBy {\n      id\n    }\n\n    oldVersions {\n      ...AdminProductOldVersion\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query AdminProductDetailPage($eventSlug: String!, $productId: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          id\n          name\n          countTotal\n        }\n\n        product(id: $productId) {\n          ...AdminProductDetail\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query AdminProductDetailPage($eventSlug: String!, $productId: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          id\n          name\n          countTotal\n        }\n\n        product(id: $productId) {\n          ...AdminProductDetail\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateProduct($input: CreateProductInput!) {\n    createProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateProduct($input: CreateProductInput!) {\n    createProduct(input: $input) {\n      product {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation ReorderProducts($input: ReorderProductsInput!) {\n    reorderProducts(input: $input) {\n      products {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation ReorderProducts($input: ReorderProductsInput!) {\n    reorderProducts(input: $input) {\n      products {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProductList on FullProductType {\n    id\n    title\n    description\n    price\n    isAvailable\n    availableFrom\n    availableUntil\n    countPaid\n    countReserved\n    countAvailable\n  }\n"): (typeof documents)["\n  fragment ProductList on FullProductType {\n    id\n    title\n    description\n    price\n    isAvailable\n    availableFrom\n    availableUntil\n    countPaid\n    countReserved\n    countAvailable\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProductList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductList\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProductList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        products {\n          ...ProductList\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateProgramBasicInfo($input: UpdateProgramInput!) {\n    updateProgram(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateProgramBasicInfo($input: UpdateProgramInput!) {\n    updateProgram(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateProgramDimensions($input: UpdateProgramDimensionsInput!) {\n    updateProgramDimensions(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateProgramDimensions($input: UpdateProgramDimensionsInput!) {\n    updateProgramDimensions(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramAdminDetailDimensionsQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      program {\n        dimensions {\n          ...DimensionRowGroup\n        }\n\n        program(slug: $programSlug) {\n          slug\n          title\n          cachedDimensions\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramAdminDetailDimensionsQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      program {\n        dimensions {\n          ...DimensionRowGroup\n        }\n\n        program(slug: $programSlug) {\n          slug\n          title\n          cachedDimensions\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramAdminDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          slug\n          title\n          description\n          cachedHosts\n\n          programOffer {\n            id\n            values\n          }\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramAdminDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          slug\n          title\n          description\n          cachedHosts\n\n          programOffer {\n            id\n            values\n          }\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProgramAdmin on FullProgramType {\n    slug\n    title\n    scheduleItems {\n      startTime\n    }\n    cachedDimensions\n  }\n"): (typeof documents)["\n  fragment ProgramAdmin on FullProgramType {\n    slug\n    title\n    scheduleItems {\n      startTime\n    }\n    cachedDimensions\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramAdminList(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        # TODO fragmentify\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isKeyDimension\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        programs(filters: $filters) {\n          ...ProgramAdmin\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramAdminList(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        # TODO fragmentify\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isKeyDimension\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        programs(filters: $filters) {\n          ...ProgramAdmin\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PutProgramDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PutProgramDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteProgramDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteProgramDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PutProgramDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PutProgramDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteProgramDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteProgramDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramDimensionsList($eventSlug: String!, $locale: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        dimensions(publicOnly: false) {\n          ...DimensionRowGroup\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramDimensionsList($eventSlug: String!, $locale: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      program {\n        dimensions(publicOnly: false) {\n          ...DimensionRowGroup\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateProgramFormLanguage($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateProgramFormLanguage($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteProgramFormLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteProgramFormLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateFormFieldsMutation($input: UpdateFormFieldsInput!) {\n    updateFormFields(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateFormFieldsMutation($input: UpdateFormFieldsInput!) {\n    updateFormFields(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PromoteProgramFormFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PromoteProgramFormFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditProgramFormFieldsPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditProgramFormFieldsPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment EditProgramFormLanguage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment EditProgramFormLanguage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditProgramFormLanguagePage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramFormLanguage\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditProgramFormLanguagePage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramFormLanguage\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateProgramFormLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateProgramFormLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateProgramFormMutation($input: UpdateSurveyInput!) {\n    updateProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateProgramFormMutation($input: UpdateSurveyInput!) {\n    updateProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteProrgamFormMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteProrgamFormMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment EditProgramForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    activeFrom\n    activeUntil\n    canRemove\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n"): (typeof documents)["\n  fragment EditProgramForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    activeFrom\n    activeUntil\n    canRemove\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditProgramFormPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramForm\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditProgramFormPage(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug, app: PROGRAM_V2) {\n          ...EditProgramForm\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateProgramForm($input: CreateProgramFormInput!) {\n    createProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateProgramForm($input: CreateProgramFormInput!) {\n    createProgramForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment OfferForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment OfferForm on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramFormsPage($eventSlug: String!, $locale: String) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      forms {\n        surveys(includeInactive: true, app: PROGRAM_V2) {\n          ...OfferForm\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramFormsPage($eventSlug: String!, $locale: String) {\n    event(slug: $eventSlug) {\n      slug\n      name\n\n      forms {\n        surveys(includeInactive: true, app: PROGRAM_V2) {\n          ...OfferForm\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation AcceptProgramOffer($input: AcceptProgramOfferInput!) {\n    acceptProgramOffer(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation AcceptProgramOffer($input: AcceptProgramOfferInput!) {\n    acceptProgramOffer(input: $input) {\n      program {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProgramOfferDetail on FullResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n      email\n    }\n    language\n    values\n    form {\n      fields\n      survey {\n        title(lang: $locale)\n        slug\n      }\n    }\n    programs {\n      slug\n      title\n    }\n    cachedDimensions\n  }\n"): (typeof documents)["\n  fragment ProgramOfferDetail on FullResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n      email\n    }\n    language\n    values\n    form {\n      fields\n      survey {\n        title(lang: $locale)\n        slug\n      }\n    }\n    programs {\n      slug\n      title\n    }\n    cachedDimensions\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramOfferPage(\n    $eventSlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      program {\n        dimensions(publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isTechnical\n          isMultiValue\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n          }\n        }\n\n        programOffer(id: $responseId) {\n          ...ProgramOfferDetail\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramOfferPage(\n    $eventSlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      slug\n      program {\n        dimensions(publicOnly: false) {\n          slug\n          title(lang: $locale)\n          isTechnical\n          isMultiValue\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n          }\n        }\n\n        programOffer(id: $responseId) {\n          ...ProgramOfferDetail\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProgramOffer on FullResponseType {\n    id\n    createdAt\n    createdBy {\n      displayName\n    }\n    sequenceNumber\n    values(keyFieldsOnly: true)\n    form {\n      survey {\n        title(lang: $locale)\n      }\n      language\n    }\n    cachedDimensions\n    programs {\n      slug\n      title\n    }\n  }\n"): (typeof documents)["\n  fragment ProgramOffer on FullResponseType {\n    id\n    createdAt\n    createdBy {\n      displayName\n    }\n    sequenceNumber\n    values(keyFieldsOnly: true)\n    form {\n      survey {\n        title(lang: $locale)\n      }\n      language\n    }\n    cachedDimensions\n    programs {\n      slug\n      title\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProgramOfferDimension on FullDimensionType {\n    slug\n    title(lang: $locale)\n    isKeyDimension\n    isTechnical\n\n    values(lang: $locale) {\n      slug\n      title(lang: $locale)\n      color\n      isTechnical\n    }\n  }\n"): (typeof documents)["\n  fragment ProgramOfferDimension on FullDimensionType {\n    slug\n    title(lang: $locale)\n    isKeyDimension\n    isTechnical\n\n    values(lang: $locale) {\n      slug\n      title(lang: $locale)\n      color\n      isTechnical\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramOffers(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        stateDimension {\n          ...ProgramOfferDimension\n        }\n\n        countProgramOffers\n        programOffers(filters: $filters) {\n          ...ProgramOffer\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramOffers(\n    $eventSlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      slug\n      name\n      program {\n        listFilters: dimensions(isListFilter: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {\n          ...ProgramOfferDimension\n        }\n\n        stateDimension {\n          ...ProgramOfferDimension\n        }\n\n        countProgramOffers\n        programOffers(filters: $filters) {\n          ...ProgramOffer\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation MarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    markScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n"): (typeof documents)["\n  mutation MarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    markScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UnmarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    unmarkScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n"): (typeof documents)["\n  mutation UnmarkScheduleItemAsFavorite($input: FavoriteScheduleItemInput!) {\n    unmarkScheduleItemAsFavorite(input: $input) {\n      success\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ScheduleProgram on LimitedProgramType {\n    slug\n    title\n    cachedDimensions\n    color\n  }\n"): (typeof documents)["\n  fragment ScheduleProgram on LimitedProgramType {\n    slug\n    title\n    cachedDimensions\n    color\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ScheduleItemList on FullScheduleItemType {\n    slug\n    location\n    subtitle\n    startTime\n    endTime\n    program {\n      ...ScheduleProgram\n    }\n  }\n"): (typeof documents)["\n  fragment ScheduleItemList on FullScheduleItemType {\n    slug\n    location\n    subtitle\n    startTime\n    endTime\n    program {\n      ...ScheduleProgram\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramListQuery(\n    $locale: String\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $hidePast: Boolean\n  ) {\n    profile {\n      program {\n        scheduleItems(\n          eventSlug: $eventSlug\n          filters: $filters\n          hidePast: $hidePast\n        ) {\n          ...ScheduleItemList\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        listFilters: dimensions(isListFilter: true) {\n          slug\n          title(lang: $locale)\n          isListFilter\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        scheduleItems(filters: $filters, hidePast: $hidePast) {\n          ...ScheduleItemList\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramListQuery(\n    $locale: String\n    $eventSlug: String!\n    $filters: [DimensionFilterInput!]\n    $hidePast: Boolean\n  ) {\n    profile {\n      program {\n        scheduleItems(\n          eventSlug: $eventSlug\n          filters: $filters\n          hidePast: $hidePast\n        ) {\n          ...ScheduleItemList\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        listFilters: dimensions(isListFilter: true) {\n          slug\n          title(lang: $locale)\n          isListFilter\n\n          values(lang: $locale) {\n            slug\n            title(lang: $locale)\n            color\n          }\n        }\n\n        scheduleItems(filters: $filters, hidePast: $hidePast) {\n          ...ScheduleItemList\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateFeedback($input: ProgramFeedbackInput!) {\n    createProgramFeedback(input: $input) {\n      success\n    }\n  }\n"): (typeof documents)["\n  mutation CreateFeedback($input: ProgramFeedbackInput!) {\n    createProgramFeedback(input: $input) {\n      success\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramFeedbackQuery($eventSlug: String!, $programSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        program(slug: $programSlug) {\n          title\n          isAcceptingFeedback\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramFeedbackQuery($eventSlug: String!, $programSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      program {\n        program(slug: $programSlug) {\n          title\n          isAcceptingFeedback\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProgramDetailAnnotation on ProgramAnnotationType {\n    annotation {\n      slug\n      type\n      title(lang: $locale)\n    }\n    value(lang: $locale)\n  }\n"): (typeof documents)["\n  fragment ProgramDetailAnnotation on ProgramAnnotationType {\n    annotation {\n      slug\n      type\n      title(lang: $locale)\n    }\n    value(lang: $locale)\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProgramDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    profile {\n      program {\n        scheduleItems(eventSlug: $eventSlug) {\n          slug\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          title\n          description\n          cachedHosts\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProgramDetailQuery(\n    $eventSlug: String!\n    $programSlug: String!\n    $locale: String\n  ) {\n    profile {\n      program {\n        scheduleItems(eventSlug: $eventSlug) {\n          slug\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n      slug\n      timezone\n\n      program {\n        calendarExportLink\n\n        program(slug: $programSlug) {\n          title\n          description\n          cachedHosts\n\n          links(lang: $locale) {\n            type\n            href\n            title\n          }\n\n          annotations(isShownInDetail: true) {\n            ...ProgramDetailAnnotation\n          }\n\n          dimensions(isShownInDetail: true) {\n            dimension {\n              slug\n              title(lang: $locale)\n            }\n            value {\n              slug\n              title(lang: $locale)\n            }\n          }\n          scheduleItems {\n            slug\n            subtitle\n            location\n            startTime\n            endTime\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateQuota($input: UpdateQuotaInput!) {\n    updateQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateQuota($input: UpdateQuotaInput!) {\n    updateQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteQuota($input: DeleteQuotaInput!) {\n    deleteQuota(input: $input) {\n      id\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteQuota($input: DeleteQuotaInput!) {\n    deleteQuota(input: $input) {\n      id\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment QuotaProduct on LimitedProductType {\n    id\n    title\n    price\n    countReserved\n  }\n"): (typeof documents)["\n  fragment QuotaProduct on LimitedProductType {\n    id\n    title\n    price\n    countReserved\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query AdminQuotaDetailPage($eventSlug: String!, $quotaId: Int!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quota(id: $quotaId) {\n          id\n          name\n          countReserved\n          quota: countTotal\n          canDelete\n\n          products {\n            ...QuotaProduct\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query AdminQuotaDetailPage($eventSlug: String!, $quotaId: Int!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quota(id: $quotaId) {\n          id\n          name\n          countReserved\n          quota: countTotal\n          canDelete\n\n          products {\n            ...QuotaProduct\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateQuota($input: CreateQuotaInput!) {\n    createQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateQuota($input: CreateQuotaInput!) {\n    createQuota(input: $input) {\n      quota {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment QuotaList on FullQuotaType {\n    id\n    title: name\n    countPaid\n    countReserved\n    countAvailable\n    countTotal\n  }\n"): (typeof documents)["\n  fragment QuotaList on FullQuotaType {\n    id\n    title: name\n    countPaid\n    countReserved\n    countAvailable\n    countTotal\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query QuotaList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          ...QuotaList\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query QuotaList($eventSlug: String!) {\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      tickets {\n        quotas {\n          ...QuotaList\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PutSurveyDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PutSurveyDimension($input: PutDimensionInput!) {\n    putDimension(input: $input) {\n      dimension {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteSurveyDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteSurveyDimension($input: DeleteDimensionInput!) {\n    deleteDimension(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PutSurveyDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PutSurveyDimensionValue($input: PutDimensionValueInput!) {\n    putDimensionValue(input: $input) {\n      value {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteSurveyDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteSurveyDimensionValue($input: DeleteDimensionValueInput!) {\n    deleteDimensionValue(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ValueFields on DimensionValueType {\n    slug\n    color\n    isInitial\n    isTechnical\n    canRemove\n    title(lang: $locale)\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n  }\n"): (typeof documents)["\n  fragment ValueFields on DimensionValueType {\n    slug\n    color\n    isInitial\n    isTechnical\n    canRemove\n    title(lang: $locale)\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment DimensionRowGroup on FullDimensionType {\n    slug\n    canRemove\n    title(lang: $locale)\n    isPublic\n    isKeyDimension\n    isMultiValue\n    isListFilter\n    isShownInDetail\n    isNegativeSelection\n    isTechnical\n    valueOrdering\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n    values {\n      ...ValueFields\n    }\n  }\n"): (typeof documents)["\n  fragment DimensionRowGroup on FullDimensionType {\n    slug\n    canRemove\n    title(lang: $locale)\n    isPublic\n    isKeyDimension\n    isMultiValue\n    isListFilter\n    isShownInDetail\n    isNegativeSelection\n    isTechnical\n    valueOrdering\n    # NOTE SUPPORTED_LANGUAGES\n    titleFi\n    titleEn\n    titleSv\n    values {\n      ...ValueFields\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query DimensionsList(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String!\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          canRemove\n          languages {\n            language\n          }\n          dimensions {\n            ...DimensionRowGroup\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query DimensionsList(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String!\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          canRemove\n          languages {\n            language\n          }\n          dimensions {\n            ...DimensionRowGroup\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateFormMutation($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateFormMutation($input: UpdateFormInput!) {\n    updateForm(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteSurveyLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteSurveyLanguage($input: DeleteSurveyLanguageInput!) {\n    deleteSurveyLanguage(input: $input) {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation PromoteSurveyFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation PromoteSurveyFieldToDimension(\n    $input: PromoteFieldToDimensionInput!\n  ) {\n    promoteFieldToDimension(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment EditSurveyFieldsPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    dimensions {\n      ...DimensionRowGroup\n    }\n\n    form(lang: $language) {\n      title\n      language\n      fields(enrich: false)\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment EditSurveyFieldsPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    dimensions {\n      ...DimensionRowGroup\n    }\n\n    form(lang: $language) {\n      title\n      language\n      fields(enrich: false)\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditSurveyFieldsPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditSurveyFieldsPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          ...EditSurveyFieldsPage\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment EditFormLanguagePage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment EditFormLanguagePage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    canRemove\n\n    form(lang: $language) {\n      title\n      language\n      description\n      thankYouMessage\n      fields\n      canRemove\n    }\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditFormLanguagePageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditFormLanguagePage\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditFormLanguagePageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $language: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditFormLanguagePage\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateSurveyLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateSurveyLanguage($input: CreateSurveyLanguageInput!) {\n    createSurveyLanguage(input: $input) {\n      form {\n        language\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateSurveyMutation($input: UpdateSurveyInput!) {\n    updateSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateSurveyMutation($input: UpdateSurveyInput!) {\n    updateSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteSurveyMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteSurveyMutation($input: DeleteSurveyInput!) {\n    deleteSurvey(input: $input) {\n      slug\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment EditSurveyPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    loginRequired\n    anonymity\n    maxResponsesPerUser\n    countResponsesByCurrentUser\n    activeFrom\n    activeUntil\n    canRemove\n    protectResponses\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n"): (typeof documents)["\n  fragment EditSurveyPage on FullSurveyType {\n    slug\n    title(lang: $locale)\n    loginRequired\n    anonymity\n    maxResponsesPerUser\n    countResponsesByCurrentUser\n    activeFrom\n    activeUntil\n    canRemove\n    protectResponses\n\n    languages {\n      title\n      language\n      canRemove\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query EditSurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditSurveyPage\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query EditSurveyPageQuery(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug, app: FORMS) {\n          ...EditSurveyPage\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UpdateResponseDimensions($input: UpdateResponseDimensionsInput!) {\n    updateResponseDimensions(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation UpdateResponseDimensions($input: UpdateResponseDimensionsInput!) {\n    updateResponseDimensions(input: $input) {\n      response {\n        id\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query SurveyResponseDetail(\n    $eventSlug: String!\n    $surveySlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n          anonymity\n          canRemoveResponses\n          protectResponses\n\n          dimensions {\n            title(lang: $locale)\n            slug\n            isTechnical\n            isMultiValue\n\n            values {\n              title(lang: $locale)\n              slug\n              color\n            }\n          }\n\n          response(id: $responseId) {\n            id\n            sequenceNumber\n            createdAt\n            createdBy {\n              displayName\n              email\n            }\n            language\n            values\n            form {\n              fields\n            }\n            cachedDimensions\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveyResponseDetail(\n    $eventSlug: String!\n    $surveySlug: String!\n    $responseId: String!\n    $locale: String\n  ) {\n    event(slug: $eventSlug) {\n      name\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          slug\n          anonymity\n          canRemoveResponses\n          protectResponses\n\n          dimensions {\n            title(lang: $locale)\n            slug\n            isTechnical\n            isMultiValue\n\n            values {\n              title(lang: $locale)\n              slug\n              color\n            }\n          }\n\n          response(id: $responseId) {\n            id\n            sequenceNumber\n            createdAt\n            createdBy {\n              displayName\n              email\n            }\n            language\n            values\n            form {\n              fields\n            }\n            cachedDimensions\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation SubscribeToSurveyResponses($input: SubscriptionInput!) {\n    subscribeToSurveyResponses(input: $input) {\n      success\n    }\n  }\n"): (typeof documents)["\n  mutation SubscribeToSurveyResponses($input: SubscriptionInput!) {\n    subscribeToSurveyResponses(input: $input) {\n      success\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation UnsubscribeFromSurveyResponses($input: SubscriptionInput!) {\n    unsubscribeFromSurveyResponses(input: $input) {\n      success\n    }\n  }\n"): (typeof documents)["\n  mutation UnsubscribeFromSurveyResponses($input: SubscriptionInput!) {\n    unsubscribeFromSurveyResponses(input: $input) {\n      success\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation DeleteSurveyResponses($input: DeleteSurveyResponsesInput!) {\n    deleteSurveyResponses(input: $input) {\n      countDeleted\n    }\n  }\n"): (typeof documents)["\n  mutation DeleteSurveyResponses($input: DeleteSurveyResponsesInput!) {\n    deleteSurveyResponses(input: $input) {\n      countDeleted\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n    }\n    language\n    values(keyFieldsOnly: true)\n    cachedDimensions(keyDimensionsOnly: true)\n  }\n"): (typeof documents)["\n  fragment SurveyResponse on LimitedResponseType {\n    id\n    sequenceNumber\n    createdAt\n    createdBy {\n      displayName\n    }\n    language\n    values(keyFieldsOnly: true)\n    cachedDimensions(keyDimensionsOnly: true)\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query FormResponses(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    profile {\n      forms {\n        surveys(eventSlug: $eventSlug, relation: SUBSCRIBED) {\n          slug\n        }\n      }\n    }\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          anonymity\n\n          fields(lang: $locale, keyFieldsOnly: true)\n          dimensions {\n            slug\n            title(lang: $locale)\n            isKeyDimension\n\n            values {\n              slug\n              title(lang: $locale)\n              color\n            }\n          }\n\n          countResponses\n          canRemoveResponses\n          protectResponses\n\n          responses(filters: $filters) {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query FormResponses(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    profile {\n      forms {\n        surveys(eventSlug: $eventSlug, relation: SUBSCRIBED) {\n          slug\n        }\n      }\n    }\n    event(slug: $eventSlug) {\n      name\n      slug\n\n      forms {\n        survey(slug: $surveySlug) {\n          slug\n          title(lang: $locale)\n          anonymity\n\n          fields(lang: $locale, keyFieldsOnly: true)\n          dimensions {\n            slug\n            title(lang: $locale)\n            isKeyDimension\n\n            values {\n              slug\n              title(lang: $locale)\n              color\n            }\n          }\n\n          countResponses\n          canRemoveResponses\n          protectResponses\n\n          responses(filters: $filters) {\n            ...SurveyResponse\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query SurveySummary(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          fields(lang: $locale)\n          summary(filters: $filters)\n          countFilteredResponses: countResponses(filters: $filters)\n          countResponses\n          dimensions {\n            slug\n            title(lang: $locale)\n            values {\n              slug\n              title(lang: $locale)\n            }\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query SurveySummary(\n    $eventSlug: String!\n    $surveySlug: String!\n    $locale: String\n    $filters: [DimensionFilterInput!]\n  ) {\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        survey(slug: $surveySlug) {\n          title(lang: $locale)\n          fields(lang: $locale)\n          summary(filters: $filters)\n          countFilteredResponses: countResponses(filters: $filters)\n          countResponses\n          dimensions {\n            slug\n            title(lang: $locale)\n            values {\n              slug\n              title(lang: $locale)\n            }\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateSurvey($input: CreateSurveyInput!) {\n    createSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation CreateSurvey($input: CreateSurveyInput!) {\n    createSurvey(input: $input) {\n      survey {\n        slug\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment Survey on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n"): (typeof documents)["\n  fragment Survey on FullSurveyType {\n    slug\n    title(lang: $locale)\n    isActive\n    activeFrom\n    activeUntil\n    countResponses\n\n    languages {\n      language\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query Surveys($eventSlug: String!, $locale: String) {\n    profile {\n      forms {\n        surveys(relation: ACCESSIBLE) {\n          event {\n            slug\n            name\n          }\n          slug\n          title(lang: $locale)\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys(includeInactive: true, app: FORMS) {\n          ...Survey\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query Surveys($eventSlug: String!, $locale: String) {\n    profile {\n      forms {\n        surveys(relation: ACCESSIBLE) {\n          event {\n            slug\n            name\n          }\n          slug\n          title(lang: $locale)\n        }\n      }\n    }\n\n    event(slug: $eventSlug) {\n      name\n\n      forms {\n        surveys(includeInactive: true, app: FORMS) {\n          ...Survey\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation GenerateKeyPair($password: String!) {\n    generateKeyPair(password: $password) {\n      id\n    }\n  }\n"): (typeof documents)["\n  mutation GenerateKeyPair($password: String!) {\n    generateKeyPair(password: $password) {\n      id\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation RevokeKeyPair($id: String!) {\n    revokeKeyPair(id: $id) {\n      id\n    }\n  }\n"): (typeof documents)["\n  mutation RevokeKeyPair($id: String!) {\n    revokeKeyPair(id: $id) {\n      id\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProfileEncryptionKeys on KeyPairType {\n    id\n    createdAt\n  }\n"): (typeof documents)["\n  fragment ProfileEncryptionKeys on KeyPairType {\n    id\n    createdAt\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProfileEncryptionKeys {\n    profile {\n      keypairs {\n        ...ProfileEncryptionKeys\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProfileEncryptionKeys {\n    profile {\n      keypairs {\n        ...ProfileEncryptionKeys\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProfileOrderDetail($eventSlug: String!, $orderId: String!) {\n    profile {\n      tickets {\n        order(eventSlug: $eventSlug, id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          canPay\n          products {\n            title\n            quantity\n            price\n          }\n\n          event {\n            slug\n            name\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProfileOrderDetail($eventSlug: String!, $orderId: String!) {\n    profile {\n      tickets {\n        order(eventSlug: $eventSlug, id: $orderId) {\n          id\n          formattedOrderNumber\n          createdAt\n          totalPrice\n          status\n          eticketsLink\n          canPay\n          products {\n            title\n            quantity\n            price\n          }\n\n          event {\n            slug\n            name\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation ConfirmEmail($input: ConfirmEmailInput!) {\n    confirmEmail(input: $input) {\n      user {\n        email\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation ConfirmEmail($input: ConfirmEmailInput!) {\n    confirmEmail(input: $input) {\n      user {\n        email\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProfileOrder on ProfileOrderType {\n    id\n    formattedOrderNumber\n    createdAt\n    totalPrice\n    status\n    eticketsLink\n    canPay\n\n    event {\n      slug\n      name\n    }\n  }\n"): (typeof documents)["\n  fragment ProfileOrder on ProfileOrderType {\n    id\n    formattedOrderNumber\n    createdAt\n    totalPrice\n    status\n    eticketsLink\n    canPay\n\n    event {\n      slug\n      name\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProfileOrders {\n    profile {\n      tickets {\n        orders {\n          ...ProfileOrder\n        }\n\n        haveUnlinkedOrders\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProfileOrders {\n    profile {\n      tickets {\n        orders {\n          ...ProfileOrder\n        }\n\n        haveUnlinkedOrders\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query ProfileSurveyResponsePage($locale: String!, $responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n\n          dimensions {\n            ...DimensionBadge\n          }\n\n          form {\n            title\n            language\n            fields\n            event {\n              slug\n              name\n            }\n            survey {\n              anonymity\n            }\n          }\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query ProfileSurveyResponsePage($locale: String!, $responseId: String!) {\n    profile {\n      forms {\n        response(id: $responseId) {\n          id\n          createdAt\n          values\n\n          dimensions {\n            ...DimensionBadge\n          }\n\n          form {\n            title\n            language\n            fields\n            event {\n              slug\n              name\n            }\n            survey {\n              anonymity\n            }\n          }\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment ProfileResponsesTableRow on ProfileResponseType {\n    id\n    createdAt\n    dimensions(keyDimensionsOnly: true) {\n      dimension {\n        slug\n        title(lang: $locale)\n      }\n\n      value {\n        slug\n        title(lang: $locale)\n        color\n      }\n    }\n    form {\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n"): (typeof documents)["\n  fragment ProfileResponsesTableRow on ProfileResponseType {\n    id\n    createdAt\n    dimensions(keyDimensionsOnly: true) {\n      dimension {\n        slug\n        title(lang: $locale)\n      }\n\n      value {\n        slug\n        title(lang: $locale)\n        color\n      }\n    }\n    form {\n      title\n      event {\n        slug\n        name\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query OwnFormResponses($locale: String!) {\n    profile {\n      forms {\n        responses {\n          ...ProfileResponsesTableRow\n        }\n      }\n    }\n  }\n"): (typeof documents)["\n  query OwnFormResponses($locale: String!) {\n    profile {\n      forms {\n        responses {\n          ...ProfileResponsesTableRow\n        }\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  fragment DimensionBadge on ResponseDimensionValueType {\n    dimension {\n      slug\n      title(lang: $locale)\n    }\n\n    value {\n      slug\n      title(lang: $locale)\n      color\n    }\n  }\n"): (typeof documents)["\n  fragment DimensionBadge on ResponseDimensionValueType {\n    dimension {\n      slug\n      title(lang: $locale)\n    }\n\n    value {\n      slug\n      title(lang: $locale)\n      color\n    }\n  }\n"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;