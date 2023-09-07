import MainViewContainer from "@/app/MainViewContainer";
import { T } from "@/translations";

interface Product {
  slug: string;
  title: string;
  description: string;
  priceCents: number;
}

async function getProducts(): Promise<Product[]> {
  return [
    {
      slug: "weekend",
      title: "Weekend ticket",
      description:
        "This ticket grants you access to the event for the whole weekend.",
      priceCents: 5000,
    },
    {
      slug: "friday",
      title: "Friday ticket",
      description:
        "This ticket grants you access to the event for Friday only.",
      priceCents: 2000,
    },
    {
      slug: "saturday",
      title: "Saturday ticket",
      description:
        "This ticket grants you access to the event for Saturday only.",
      priceCents: 4000,
    },
    {
      slug: "sunday",
      title: "Sunday ticket",
      description:
        "This ticket grants you access to the event for Sunday only.",
      priceCents: 3000,
    },
  ];
}

export default async function TicketsView() {
  const t = T((r) => r.TicketsView);
  const tCommon = T((r) => r.Common);
  const products = await getProducts();
  return (
    <MainViewContainer>
      <h1 className="mb-4">{t((r) => r.title)}</h1>

      <table className="table table-striped mb-4">
        <thead>
          <tr className="row">
            <th className="col-8">{t((r) => r.productsTable.product)}</th>
            <th className="col">{t((r) => r.productsTable.price)}</th>
            <th className="col">{t((r) => r.productsTable.quantity)}</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.slug} className="row">
              <td className="col-8">
                <p>
                  <strong>{product.title}</strong>
                </p>
                {product.description}
              </td>
              <td className="col">{product.priceCents / 100} €</td>
              <td className="col">
                <input type="number" className="form-control" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mb-4">
        <h2>{t(r => r.contactForm.title)}</h2>
        <div className="mb-3">
          <label htmlFor="firstName" className="form-label">{tCommon((r) => r.formFields.firstName.title)}</label>
          <input
            type="firstName"
            className="form-control"
            id="firstName"
            name="firstName"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="lastName" className="form-label">{tCommon((r) => r.formFields.lastName.title)}</label>
          <input
            type="lastName"
            className="form-control"
            id="lastName"
            name="lastName"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">{tCommon((r) => r.formFields.email.title)}</label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            aria-describedby="emailHelp"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="phone" className="form-label">
            Password
          </label>
          <input
            type="text"
            className="form-control"
            id="phone"
            name="phone"
          />
        </div>
        <div className="mb-3 form-check">
          <input
            type="checkbox"
            className="form-check-input"
            id="exampleCheck1"
          />
          <label className="form-check-label" htmlFor="exampleCheck1">
            Check me out
          </label>
        </div>
      </div>

      <div className="d-grid gap-2">
        <button className="btn btn-primary btn-lg">Purchase</button>
      </div>
    </MainViewContainer>
  );
}
