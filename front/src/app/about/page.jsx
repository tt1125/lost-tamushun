export default function About() {
    return (
        <div style={{ height: "100%", backgroundColor: "#010101", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <div style={{ color: "#fff" }}>
                <h1>About</h1>
                <p>画像をパラレルワールドに変換するアプリです。</p>
                <p>変換した画像はみんなで共有できます。
                    <br></br>共有した画像は、他のユーザーが見ることができます。
                    <br></br>変換した画像を元の画像と見比べてみましょう！
                </p>
                <p>このアプリに使用している技術は、以下の通りです。
                    <li>React</li>
                    <li>Flask</li>
                    <li>Novel AI API</li>
                    <li>functons</li>
                    <li>store & blob storage</li>
                </p>
                <p>Reactは、Facebookが開発したJavaScriptライブラリで、コンポーネント指向のUIライブラリです。</p>
                <p>Flaskは、PythonのWebアプリケーションフレームワークです。</p>
                <p>Novel AI APIは、画像生成AIを提供しているAPIです。</p>
                <p>functionsは、サーバーレスアーキテクチャを提供しているサービスです。</p>
                <p>store & blob storageは、画像を保存するためのストレージです。</p>



            </div>

        </div>

    )
}