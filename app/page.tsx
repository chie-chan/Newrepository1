'use client'

import { useState } from "react"

export default function FileUploadForm() {
  // カテゴリ、開始価格、即決価格を管理するstate
  const [category, setCategory] = useState("")
  const [startPrice, setStartPrice] = useState("")
  const [immediatePrice, setImmediatePrice] = useState("")

  // 実行ボタンが押されたときに呼ばれる関数
  const handleRun = async () => {
    // 送信するパラメータをオブジェクトにまとめる
    const params = {
      category: category,
      start_price: startPrice,
      sokketu: immediatePrice
    }

    try {
      // fetchでクラウド上のFastAPIへPOSTリクエスト送信
      const res = await fetch('https://myapp-latest-s07m.onrender.com/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(params)
      })
      
      // レスポンスをJSONとして読み込み
      const result = await res.json()

      // 開発者コンソールに出力
      console.log('サーバーからのレスポンス:', result)

      // ブラウザ画面にアラート表示
      alert("サーバー側で処理が完了しました: " + JSON.stringify(result))

    } catch (error) {
      console.error("エラーが発生しました:", error)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">テスト用フォーム</h2>
      <div className="space-y-4">

        <div>
          <label className="block mb-1">カテゴリ</label>
          <input 
            type="text" 
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="border p-1 rounded w-64"
            placeholder="カテゴリを入力"
          />
        </div>

        <div>
          <label className="block mb-1">開始価格</label>
          <input 
            type="text" 
            value={startPrice} 
            onChange={(e) => setStartPrice(e.target.value)}
            className="border p-1 rounded w-64"
            placeholder="開始価格を入力"
          />
        </div>

        <div>
          <label className="block mb-1">即決価格</label>
          <input 
            type="text" 
            value={immediatePrice} 
            onChange={(e) => setImmediatePrice(e.target.value)}
            className="border p-1 rounded w-64"
            placeholder="即決価格を入力"
          />
        </div>

        <button
          onClick={handleRun}
          className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
        >
          サーバーに送信
        </button>
      </div>
    </div>
  )
}



