import "./Layout.scss";

export default function Layout({ children, ...props }) {
    return <div {...props}>{children}</div>;
}
