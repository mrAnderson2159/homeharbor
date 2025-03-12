// frontend/src/components/Layout/PageContainer.jsx

export default function PageContainer({ children, className = "", ...props }) {
    return (
        <div className={`container-fluid h-100 p-0 ${className}`} {...props}>
            {children}
        </div>
    );
}
