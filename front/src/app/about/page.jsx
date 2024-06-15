export default function About() {
    return (
        <div style={{ height: "100%", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <div style={{ color: "black" }}>
                <h1>About</h1>
                <p>画像をパラレルワールドに変換するアプリです。</p>
                <p>画像はみんなで共有できます。
                    <br></br>共有した画像は、他のユーザーも見ることができます。
                    <br></br>変換した画像と元の画像とを見比べてみてください！
                </p>

                <h3>タブについて</h3>

                <li>Home：他の人が投稿した画像を見ることができます</li>
                <li>Create：画像を変換することができます</li>
                <li>Profile：プロフィールの編集ができます</li>
                <li>Chat：チャットができます</li>
                <li>About：このアプリについての説明が見れます</li>

                <h3>使用している技術</h3>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div>

                        <ul>
                            <li>React</li>
                            <li>Flask</li>
                            <li>Novel AI API</li>
                            <li>functons</li>
                            <li>store & blob storage</li>
                        </ul>
                    </div>
                    <div>
                        <ul style={{ listStyleType: 'none' }}>
                            <li>Facebookが開発したJavaScriptライブラリで、コンポーネント指向のUIライブラリです。</li>
                            <li>PythonのWebアプリケーションフレームワークです。</li>
                            <li>画像生成AIを提供しているAPIです。</li>
                            <li>サーバーレスアーキテクチャを提供しているサービスです。</li>
                            <li>画像を保存するためのストレージです。</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}