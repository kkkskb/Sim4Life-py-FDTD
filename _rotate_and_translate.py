import s4l_v1 as s4l
import s4l_v1.math as s4l_math

def rotate_and_translate_object(
	object_name: str,
	rotation_axis: s4l.Vec3,
	rotation_angle_deg: float,
	translation_vector: s4l.Vec3
):
	"""
	指定されたオブジェクトを回転させ、その後、平行移動させる関数。
	"""
	try:
		# オブジェクトを取得
		obj = s4l.get_project().get_child(object_name)
		if not obj:
			# 日本語を削除
			print(f"Error: Object named '{object_name}' not found.")
			return

		# 日本語を削除
		print(f"Applying rotation and translation to '{object_name}'...")

		# 1. 回転変換を作成
		angle_in_rad = s4l_math.radians(rotation_angle_deg)
		rotation_transform = s4l.Rotation(rotation_axis, angle_in_rad)

		# 2. 平行移動変換を作成
		translation_transform = s4l.Translation(translation_vector)

		# 3. 2つの変換を組み合わせる
		combined_transform = translation_transform * rotation_transform

		# 4. オブジェクトに結合された変換を適用
		obj.transform(combined_transform)
		# 日本語を削除
		print(f"Operation on '{object_name}' completed.")

	except Exception as e:
		# 日本語を削除
		print(f"An error occurred during script execution: {e}")

# --- スクリプトの使用例 ---
if __name__ == "__main__":
	target_object_name = "Block 1"
	rot_axis = s4l.Vec3(0, 0, 1)
	rot_angle_deg = 90.0
	trans_vec = s4l.Vec3(50, 20, 10)

	rotate_and_translate_object(
		object_name=target_object_name,
		rotation_axis=rot_axis,
		rotation_angle_deg=rot_angle_deg,
		translation_vector=trans_vec
	)